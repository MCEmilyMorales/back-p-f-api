from fastapi import FastAPI, HTTPException, Query
from app.api.database import db
from app.api.image import crud
import uuid

def add_imagen_routes(app: FastAPI):
    
    @app.post("/imagenes/")
    async def create_imagen(
        ubicacion: str = Query(..., min_length=5, max_length=255),
        informe_id: str = Query(..., min_length=36, max_length=36)
    ):
        """Guardar una imagen en la base de datos.
        Recibe: ubicacion e ID del informe del estudio al que pertenece.
        Retorna: mensaje que confirma creacion con el id. 
        """
        # Validar si informe_id es UUID
        try:
            uuid.UUID(informe_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID de informe invalido, debe tener 36 caracteres.")
        new_imagen = await crud.create_imagen(db, ubicacion, informe_id)
        return {"imagen creada con id = ": new_imagen.id}


    @app.get("/imagenes/{imagen_id}")
    async def get_imagen(imagen_id: str):
        """Obtener un imagen por ID.
        Recibe: ID de la imagen. 
        Retorna: ubicacion e ID del informe de la imagen buscada."""
        # Validar si el id de la imagen es UUID
        try:
            uuid.UUID(imagen_id)
        except ValueError:
            raise HTTPException(status_code=400, detail= "ID de la imagen invalido, debe tener 36 caracteres")
        
        imagen = await crud.get_imagen(db, imagen_id)
        if not imagen:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return {"id": imagen.id, "ubicacion": imagen.ubicacion, "informe_id": imagen.informeId}
 

    @app.get("/imagenes/{informe_id}")
    async def list_imagenes(informe_id: str):
        """ Obtener la lista de imagenes para un informe especifico.
        Retorna: lista de diccionarios (ubicacion, Id Informe)"""
        imagenes = await crud.get_imagenes_by_informe(db, informe_id)
        if not imagenes:
            raise HTTPException(status_code=404, detail="No se encontraron imágenes para este informe")
        return [{"id": img.id, "ubicacion": img.ubicacion, "informe_id": img.informeId} for img in imagenes]


    @app.delete("/imagenes/{imagen_id}")
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