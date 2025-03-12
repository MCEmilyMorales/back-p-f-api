from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from app.api.database import db
from app.api.image import crud
import uuid
import boto3
import os
from dotenv import load_dotenv


s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

def add_imagen_routes(app: FastAPI):

    @app.post("/upload/", tags=["Imágenes"])
    async def upload_imagen(informe_id: str, file: UploadFile = File(...)):
        """Sube una imagen a AWS S3 y la guarda en la BD"""
        file_location = f"imagenes-dg-prueba/{file.filename}"
        try:
            # Subir archivo a S3
            s3_client.upload_fileobj(file.file, BUCKET_NAME, file_location)
            # Guardar en la base de datos
            new_imagen = await crud.create_imagen(db, file_location, informe_id)
            return {"message": "Imagen subida con éxito", "imagen": new_imagen}
        except Exception as e:
            return {"error": str(e)}


    @app.get("/imagenes/{imagen_id}", tags=["Imágenes"])
    async def get_imagen(imagen_id: str):
        """Obtiene la URL de una imagen desde AWS S3"""
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

        deleted = await crud.delete_imagen(db, imagen_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return {"message": "Imagen eliminada"}