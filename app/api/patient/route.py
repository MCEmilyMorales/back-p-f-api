import uuid
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.api.database import db  
from app.api.patient import crud
from app.api.patient.models import PacienteCreate


def add_paciente_routes(app:FastAPI):
    @app.post("/paciente/", tags=["Paciente"])
    async def create_paciente(paciente: PacienteCreate):
        """Permite insertar a un nuevo paciente en la base de datos.
        Recibe: instancia de base de datos, nombre y id del medico (usuario).
        retorna un mensaje de que el paciente fue cargado con exito"""
        # Validar si id es UUID
        try:
            uuid.UUID(paciente.usuario_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        nuevo_paciente = await crud.create_paciente(db, paciente.nombre, paciente.usuario_id)
        if not nuevo_paciente:
            raise HTTPException(status_code=404, detail="No se pudo crear el paciente porque no existe el usuario asociado")
        return {"Paciente creado con exito."}
    
    @app.get("/paciente/", tags=["Paciente"])
    async def get_all_paciente():
        """ Conseguir a un objeto de pacientes de la base de datos.
        Retorna un objeto de pacientes."""
        paciente = await crud.get_all_pacientes(db)
        return paciente
    
    @app.get("/paciente/{paciente_id}", tags=["Paciente"])
    async def get_id_paciente(paciente_id: str):
        """ Conseguir 1 paciente de la base de datos por medio del id.
        Retorna el dato del paciente."""
        paciente = await crud.get_paciente_id(db, paciente_id)
        return paciente
    
    @app.get("/paciente/user_id/{user_id}", tags=["Paciente"])
    async def list_paciente_por_doctor(user_id: str):
        """ Conseguir 1 paciente de la base de datos por medio del id.
        Retorna el dato del paciente."""
        paciente = await crud.list_paciente_por_doctor(db, user_id)
        return paciente    
    
    @app.delete("/paciente/{paciente_id}", tags=["Paciente"])
    async def delete_paciente(paciente_id:str):
        """ Eliminar un paciente por su id.
        Retorna: mensaje de confirmacion de eliminado"""
        paciente_eliminado= await crud.delete_paciente_id(db, paciente_id)
        return {"message": "Paciente eliminado"}
    