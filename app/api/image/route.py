#import json
import json
from typing import List
import httpx
import requests
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, Response
from app.api.database import db
from app.api.image import crud
import boto3
import os
import uuid
from app.api.image import calculos

CONDASERVER_URL = "http://localhost:9000/procesar_imagen/"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def add_imagen_routes(app: FastAPI):

    @app.post("/upload/", tags=["Imágenes"])
    async def upload_imagen(
        informe_id: str = Form(...), 
        files: List[UploadFile] = File(...)
    ):
        """
        Sube varias imágenes a AWS S3, las envía al servidor de IA (Conda) y 
        guarda la respuesta en S3.
        """
        imagenes_rutas_guardadas = []
        errores = []

        async with httpx.AsyncClient() as client:
            for file in files:
                try:
                    # Generar ruta en S3
                    new_name= await crud.generar_nombre_archivo(db, informe_id)
                    file_location = f"imagenes-dg-prueba/{new_name}{file.filename}"
                    s3_client.upload_fileobj(file.file, BUCKET_NAME, file_location )

                    #data
                    response = requests.post(CONDASERVER_URL, json={"ubicacion": file_location})

                    if response.status_code != 200:
                        return {"error": "Error en la comunicación con el servidor de procesamiento."}
                    
                    # Obtener el JSON de respuesta
                    json_data = response.json()
                    resultadoFinal= calculos.PorcentajePositivos(json_data)
                    print(resultadoFinal)

                    # Guardar respuesta en S3
                    json_key = f"procesados/{new_name}.json"
                    s3_client.put_object(
                        Bucket=BUCKET_NAME,
                        Key=json_key,
                        Body=json.dumps(json_data),
                        ContentType="application/json"
                    )

                    # Guardar en la base de datos
                    new_imagen = await crud.create_imagen(db, file_location, informe_id)
                    #return {"message": "Imagen subida con éxito", "imagen": new_imagen}
                

                except Exception as e:
                    errores.append(f"Error con {file.filename}: {str(e)}")

        return {
            "message": "Proceso completado",
            "errores": errores
        }

    @app.get("/imagenes/{imagen_id}", tags=["Imágenes"])
    async def get_imagen(imagen_id: str):
        """Obtiene la URL de una imagen desde AWS S3
        Recibe: id de imagen. 
        Retorna: URL"""
        imagen = await crud.get_imagen(db, imagen_id)
        
        if not imagen:
            return {"error": "Imagen no encontrada"}
        # Generar URL prefirmada
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": imagen.ubicacion},
            ExpiresIn=3600  # Expira en 1 hora
        )
        return {"url": url}


    @app.get("/imagenes/descargar/{imagen_id}", tags=["Imágenes"])
    async def descargar_imagen(imagen_id: str):
        """Descarga una imagen directamente desde AWS S3.
        Recibe: id de imagen.
        Retorna: archivo de imagen en la respuesta.
        """
        imagen = await crud.get_imagen(db, imagen_id)
        if not imagen:
            return {"error": "Imagen no encontrada"}

        try:
            # Descargar el archivo desde S3
            s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=imagen.ubicacion)
            contenido = s3_response["Body"].read()
            content_type = s3_response["ContentType"]  # Detecta el tipo de archivo
            #attachment -> Fuerza descargar archivo, inline -> intenta abrir imagen en navegador e interpretar como texto (no util en este caso) 
            return Response(content=contenido, media_type=content_type,
                headers={"Content-Disposition": f"attachment; filename={imagen.ubicacion.split('/')[-1]}"})
        except Exception as e:
            return {"error": str(e)}
        
    @app.get("/imagenes/informe_id/{informe_id}", tags=["Imágenes"])
    async def list_imagenes(informe_id: str):
        """ Obtener la lista de imagenes para un informe especifico.
        Retorna: lista de diccionarios (ubicacion, Id Informe)"""
        imagenes = await crud.get_imagenes_by_informe(db, informe_id)
        if not imagenes:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes para este informe")
        return [{"id": img.id, "ubicacion": img.ubicacion, "informe_id": img.informeId} for img in imagenes]


    @app.delete("/imagenes/{imagen_id}", tags=["Imágenes"])
    async def delete_imagen(imagen_id: str):
        """ Eliminar una imagen.
        Recibe: id de imagen a eliminar. 
        Retorna: mensaje que notifica si se elimina"""
        # Validar si el id de la imagen es UUID
        try:
            uuid.UUID(imagen_id)
        except ValueError:
            raise HTTPException(status_code=400, detail= "ID de la imagen invalido, debe tener 36 caracteres")   
        #antes de eliminar la imagen la busco segun la ubicacion.
        imagen= await crud.get_imagen(db, imagen_id)
        if not imagen:
            raise HTTPException(status_code=404, detail="Imagen no encontrada en la base de datos")
        
        nombre_archivo = imagen.ubicacion
        deleted = await crud.delete_imagen(db, imagen_id)

        if deleted:
            try:
                s3_client.delete_object(Bucket=BUCKET_NAME, Key=nombre_archivo)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen en S3: {str(e)}")
            return {"message": "Imagen eliminada"}
        
        return {"message": "Imagen eliminada"}