from fastapi import APIRouter, HTTPException
from app.api.database import db  # ✅ Importar la conexión de main.py
from app.api.patient.paciente_shema import PacienteCreate
from app.api.patient.crud import create_paciente
router = APIRouter()


@router.post("/", summary="Crear un paciente", description="Crea un paciente con nombre.")
async def crear_paciente(paciente: PacienteCreate):
    """Permite inserta a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y la fecha de muestra.
    retorna un mensaje de que el paciente fue cargado con exito"""
    if not db.is_connected():
        await db.connect()  # 🔹 Asegurar que está conectado    
    nuevo_paciente = await create_paciente(db, paciente)
    return nuevo_paciente
