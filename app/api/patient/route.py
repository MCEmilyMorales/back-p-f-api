from fastapi import FastAPI
from app.api.database import db  # ✅ Importar la conexión de main.py
from app.api.patient import crud

def add_paciente_routes(app:FastAPI):
    @app.post("/paciente/", tags=["Paciente"])
    async def create_paciente(nombre:str):
        """Permite inserta a un nuevo paciente en la base de datos.
        Recibe: instancia de base de datos, nombre y la fecha de muestra.
        retorna un mensaje de que el paciente fue cargado con exito"""
        nuevo_paciente = await crud.create_paciente(db, nombre)
        return {"Paciente creado con exito."}
    
    @app.get("/paciente/", tags=["Paciente"])
    async def get_all_paciente():
        """ Conseguir a un objeto de pacientes de la base de datos.
        Retorna un objeto de pacientes."""
        informes = await crud.get_all_pacientes(db)
        return informes
    
    @app.get("/paciente/{paciente_id}", tags=["Paciente"])
    async def get_id_paciente(paciente_id: str):
        """ Conseguir 1 paciente de la base de datos por medio del id.
        Retorna el dato del paciente."""
        informe = await crud.get_paciente_id(db, paciente_id)
        return informe
    
    @app.delete("/paciente/{paciente_id}", tags=["Paciente"])
    async def delete_paciente(paciente_id:str):
        """ Eliminar un paciente por su id.
        Retorna: mensaje de confirmacion de eliminado"""
        paciente_eliminado= await crud.delete_paciente_id(db, paciente_id)
        return {"message": "Paciente eliminado"}
    