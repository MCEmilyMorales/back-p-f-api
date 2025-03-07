from fastapi import FastAPI
from app.api.database import db
from app.api.informe import crud

def add_informe_routes(app: FastAPI):
    @app.post("/informe/", tags=["Informe"])
    async def create_informe(fecha_de_muestra:str,pacienteId:str, imagenes):
        """Permite insertar a un nuevo informe en la base de datos.
        Recibe: instancia de base de datos, fecha de muestra, pacienteId e imagenes.
        retorna un mensaje de que el informe fue cargado con exito"""
        await crud.create_informe(db, fecha_de_muestra, pacienteId,imagenes)

    @app.get("/informe/", tags=["Informe"])
    async def list_informes():
        """ Conseguir un objeto de informes.
        Retorna: lista de diccionarios"""
        informes = await crud.get_all_informes(db)
        return informes
    
    @app.get("/informe/{informe_id}", tags=["Informe"])
    async def get_informe_id(informe_id:str):
        """ Conseguir 1 informe segun su id."""
        informe = await crud.get_informe_id(db, informe_id)
        return informe
    
    @app.delete("/informe/{informe_id}", tags=["Informe"])
    async def delete_informe_id(informe_id:str):
        """ Eliminar 1 informe segun su id."""
        await crud.delete_informe_id(db, informe_id)
        return {"message":"Informe eliminado con exito"}