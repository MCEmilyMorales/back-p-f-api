import uuid
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.api.database import db  
from app.api.patient import crud
from app.api.patient.models import PacienteCreate
from app.api.user import crud as crudUser
from typing import Optional

def add_paciente_routes(app:FastAPI):
    @app.post("/paciente/", tags=["Paciente"])
    async def create_paciente(paciente: PacienteCreate):
        """Permite insertar a un nuevo paciente en la base de datos.
        Recibe: instancia de base de datos, nombre, historia clinica y id del medico (usuario).
        retorna un mensaje de que el paciente fue cargado con exito"""
        IDuser = await crudUser.get_id_user(db, paciente.mail)
        if not IDuser :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        nuevo_paciente = await crud.create_paciente(db, paciente, IDuser )
        
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
        Recibe: id del paciente.
        Retorna el dato del paciente."""
        paciente = await crud.get_paciente_id(db, paciente_id)
        return paciente
    
    
    @app.get("/paciente/user_id/{user_id}", tags=["Paciente"])
    async def list_paciente_por_doctor(user_id: str):
        """ Conseguir 1 paciente de la base de datos por medio del id.
        Recibe: id del usuario.
        Retorna el dato del paciente."""
        paciente = await crud.list_paciente_por_doctor(db, user_id)
        return paciente    
    

    #Buscar paciente por DNI o SEXO o FECHA_DE_NACIMIENTO:
    @app.get("/paciente_dni_sexo", tags=["Paciente"])
    async def get_dni_paciente(paciente_dni: str= Depends(crud.validar_dni), paciente_sexo: Optional[str] = Depends(crud.validar_sexo), paciente_fecha_de_nacimiento:Optional[str] = Depends(crud.validar_fecha_de_nacimiento)):
        """ Conseguir 1 paciente de la base de datos por medio del dni, del sexo o la fecha de nacimiento.
        Recibe: obligatorio: dni del paciente, opcional:sexo, fecha de nacimiento.
        Retorna el datos del paciente."""
        if paciente_sexo:
            paciente = await crud.get_paciente_dni_sexo(db, paciente_dni, paciente_sexo)
        elif paciente_fecha_de_nacimiento: 
            paciente = await crud.get_paciente_fecha_de_nacimiento(db, paciente_dni, paciente_sexo, paciente_fecha_de_nacimiento)
        else:
            paciente = await crud.get_paciente_dni(db, paciente_dni)
        return paciente
    
    @app.delete("/paciente/{paciente_id}", tags=["Paciente"])
    async def delete_paciente(paciente_id:str):
        """ Eliminar un paciente por su id.
        Recibe: id del paciente.
        Retorna: mensaje de confirmacion de eliminado"""
        paciente_eliminado= await crud.delete_paciente_id(db, paciente_id)
        return {"message": "Paciente eliminado"}
    