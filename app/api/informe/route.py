import json
import uuid
from fastapi import FastAPI, HTTPException
from app.api.database import db
from app.api.informe import crud
from app.api.informe.models import InformeCreate, InformeUpdatePromedio

def add_informe_routes(app: FastAPI):
    @app.post("/informe/", tags=["Informe"])
    async def create_informe(informeCreate: InformeCreate):
        """Permite insertar a un nuevo informe en la base de datos.
        Recibe: instancia de base de datos, fecha de muestra, pacienteId e imagenes.
        retorna un mensaje de que el informe fue cargado con exito"""
        informe = await crud.create_informe(db, informeCreate)
        return informe

    @app.get("/informe/", tags=["Informe"])
    async def list_informes():
        """ Conseguir un objeto de informes.
        Retorna: lista de diccionarios"""
        informes = await crud.get_all_informes(db)
        return informes
    
    @app.get("/informe/{informe_id}", tags=["Informe"])
    async def get_informe_id(informe_id:str):
        """ Conseguir 1 informe segun su id."""
        return await crud.get_informe_id(db, informe_id)

    @app.get("/informe/paciente_id/{paciente_id}", tags=["Informe"])
    async def list_informes_por_paciente(paciente_id: str):
        informes= await crud.list_informes_por_paciente(db, paciente_id) 
        return informes 
    
    @app.put("/informe/{informe_id}", tags=["Informe"])
    async def update_promedio_rta_img(InformeUpdatePromedio:InformeUpdatePromedio):
        """Permite actualizar el promedio de resultado de las imagenes.
        Parametro: modelo de informe con id y json.
        Retorna: mensaje de exito de actualizacion o mensaje de error."""
        try:
            uuid.UUID(InformeUpdatePromedio.id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        #json_string = json.dumps(InformeUpdatePromedio.promedio_rta_img)
        json_string = InformeUpdatePromedio.promedio_rta_img
        promedioUpdate = await crud.update_promedio(db, InformeUpdatePromedio.id, json_string)
        if not promedioUpdate:
            raise HTTPException(status_code=404, detail="No se pudo encontrar el informe para actualizar promedio")
        return {"promedio actualizado correctamente"}
    
    @app.delete("/informe/{informe_id}", tags=["Informe"])
    async def delete_informe_id(informe_id:str):
        """ Eliminar 1 informe segun su id."""
        await crud.delete_informe_id(db, informe_id)
        return {"message":"Informe eliminado con exito"}