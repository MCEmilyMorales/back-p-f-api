import os
from typing import List, Dict
from fastapi import Request, BackgroundTasks,WebSocket, WebSocketDisconnect, FastAPI, File, Form, HTTPException, UploadFile, Response
from fastapi.responses import HTMLResponse
from app.api.database import db
from app.api.image import crud
import boto3
import uuid
from app.api.informe import crud as crud_informe
from app.api.image.websocket.procesar_imagen import run_async_procesar
#!prueba
import asyncio
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
#!fin_prueba
CONDASERVER_URL = "http://localhost:9000/procesar_imagen/"
#CONDASERVER_URL = "http://3.145.154.40:9000/procesar_imagen/"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
# Diccionario temporal para almacenar websockets activos por job_id
active_connections: Dict[str, WebSocket] = {}

def add_imagen_routes(app: FastAPI):
#!prueba
    templates = Jinja2Templates(directory="templates")

    @app.get("/test-ws", response_class=HTMLResponse)
    async def websocket_test(request: Request):
        return templates.TemplateResponse("ws_test.html", {"request": request})
#!fin_prueba
    @app.get('/')
    async def get():
        print('⏬ :', HTMLResponse()) 
        
        return HTMLResponse()

    @app.post("/upload/", tags=["Imágenes"])
    async def upload_imagen(background_tasks: BackgroundTasks, informe_id: str = Form(...), files: List[UploadFile] = File(...)):
        """
        Sube varias imágenes a AWS, analiza con servidor IA (Conda) y guarda la rta (json) en S3.
        Recibe: el id informe al que pertenecen las imagenes y archivos imagen
        Retorna: json con respuesta del modelo + interpretaciones
        """
        # Validar si el id del informe es UUID
        try:
            uuid.UUID(informe_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de informe invalido, debe ser UUID de 36 caracteres")

        # validamos existencia del informe
        informe_id_valido = await crud_informe.get_informe_id(db, informe_id)

        job_ids = []
        for file in files:
            # Crear el nombre de la imagen antes de guardar a la BD
            new_name = await crud.generar_nombre_archivo(db, informe_id_valido.id)
            file_location = f"imagenes-dg-prueba/{new_name}{file.filename}"

            print(f"🗃️ Imagen creada")
            new_imagen = await crud.create_imagen(db, file_location, informe_id_valido.id)
            print(f"🗃️ Imagen creada en BD con ID: {new_imagen.id}")
            file_bytes = await file.read()
            # Lanza el procesamiento en segundo plano de forma segura
            background_tasks.add_task(run_async_procesar,file_location, new_imagen.id, file_bytes, informe_id_valido.id)
            
            job_ids.append(new_imagen.id)
        return {"job_ids": job_ids}


    @app.websocket("/ws/{job_id}")
    async def websocket_job_status(websocket:WebSocket, job_id:str):
        await websocket.accept()
        active_connections[job_id] = websocket  # guardás la conexión activa
        try:
            while True:
                print(f"🍀 WebSocket aceptado para job_id: {job_id}")
                await websocket.receive_text()  # mantiene la conexión abierta 
        except WebSocketDisconnect:
            print(f"Cliente desconectado:🍀1 : {job_id}")
            active_connections.pop(job_id, None)
    
    
    
    @app.get("/imagenes/{imagen_id}", tags=["Imágenes"])
    async def get_imagen(imagen_id: str):
        """Obtiene la URL de una imagen desde AWS S3
        Recibe: id de imagen. 
        Retorna: URL"""
        try:
            uuid.UUID(imagen_id)
        except ValueError:
            raise HTTPException(status_code=400, detail= "ID de imagen invalido, debe ser UUID de 36 caracteres")   

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
        try:
            uuid.UUID(imagen_id)
        except ValueError:
            raise HTTPException(status_code=400, detail= "ID de imagen invalido, debe ser UUID de 36 caracteres")   

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
            return {"error al descargar el archivo desde S3": str(e)}


    @app.get("/imagenes/informe_id/{informe_id}", tags=["Imágenes"])
    async def list_imagenes(informe_id: str):
        """ Obtener la lista de imagenes para un informe especifico.
        Retorna: lista de diccionarios (ubicacion, Id Informe)"""
        # Validar si el id del informe es UUID
        try:
            uuid.UUID(informe_id)
        except ValueError:
            raise HTTPException(status_code=400, detail= "ID de informe invalido, debe ser UUID de 36 caracteres")   

        #validamos existencia del informe
        await crud_informe.get_informe_id(db, informe_id)

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
    
    
    
    
    
    #     @app.post("/upload/", tags=["Imágenes"])
    # async def upload_imagen(informe_id: str = Form(...), files: List[UploadFile] = File(...)):
    #     """
    #     Sube varias imágenes a AWS, analiza con servidor IA (Conda) y guarda la rta (json) en S3.
    #     Recibe: el id informe al que pertenecen las imagenes y archivos imagen 
    #     Retorna: json con respuesta del modelo + interpretaciones
    #     """
    #     Validar si el id del informe es UUID
    #     try:
    #         uuid.UUID(informe_id)
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail= "ID de informe invalido, debe ser UUID de 36 caracteres")   

    #     #validamos existencia del informe
    #     await crud_informe.get_informe_id(db, informe_id)

    #     resultadosFinales=[]
    #     errores = []
    #     async with httpx.AsyncClient() as client:
    #         for file in files:
    #             try:
    #                 # Subir imagen en S3
    #                 new_name= await crud.generar_nombre_archivo(db, informe_id)
    #                 file_location = f"imagenes-dg-prueba/{new_name}{file.filename}"
    #                 s3_client.upload_fileobj(file.file, BUCKET_NAME, file_location )

    #                 #comunicacion modelo ki67
    #                 response = requests.post(CONDASERVER_URL, json={"ubicacion": file_location})
    #                 if response.status_code != 200:
    #                     return {"error": "Error en la comunicación con el servidor de procesamiento."}
                    
    #                 # Obtener el JSON de respuesta
    #                 json_data = response.json()
    #                 resultadosFinales.append(calculos.PorcentajePositivos(json_data))
                    
    #                 # Guardar respuesta en S3
    #                 json_key = f"procesados/{new_name}.json"
    #                 s3_client.put_object( Bucket = BUCKET_NAME, Key = json_key, Body = json.dumps(json_data), ContentType = "application/json")

    #                 # Guardar en la base de datos PostgreSQL
    #                 new_imagen = await crud.create_imagen(db, file_location, informe_id)
    #                 new_imagen.id
    #             except Exception as e:
    #                 errores.append(f"Error con {file.filename}: {str(e)}")

    #     return {"respuesta":resultadosFinales}
