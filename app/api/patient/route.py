from fastapi import FastAPI
from app.api.database import db  # ✅ Importar la conexión de main.py
from app.api.patient.crud import create_paciente

async def add_paciente_routes(paciente):
    """Permite inserta a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y la fecha de muestra.
    retorna un mensaje de que el paciente fue cargado con exito"""
     
    nuevo_paciente = await create_paciente(db, paciente)
    return nuevo_paciente
