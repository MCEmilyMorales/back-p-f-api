from prisma.models import Informe
from prisma import Prisma
from typing import List
from datetime import datetime

async def create_informe(db: Prisma, fecha_de_muestra:str, pacienteId:str,imagenes: List[str]) -> Informe:
    """Permite insertar un nuevo informe de un paciente en la base de datos.
    Recibe: instancia de base de datos, fecha de muestra, pacienteId, y un array de imagenes."""

 # Convertir la fecha a formato ISO 8601 con hora
    fecha_iso = datetime.fromisoformat(fecha_de_muestra).isoformat()  # "2025-03-06T00:00:00"

    # Convertir imagenes a la estructura correcta para Prisma
    imagenes_data = [{"id": img_id} for img_id in imagenes]

    await db.informe.create(data={"fecha_de_muestra":fecha_iso, "pacienteId":pacienteId,"imagenes": {"connect": imagenes_data}})  # Conectar imágenes existentes
    return {"Informe creado con exito"}

async def get_all_informes(db: Prisma):
    """ Conseguir todos los informes de la base de datos.
    Retorna: lista de objetos de informes."""
    return await db.informe.find_many()

async def get_informe_id(db: Prisma, informe_id: str)-> Informe:
    """ Conseguir a 1 informe de la base de datos segun su id"""
    return await db.informe.find_unique(where={"id": informe_id})

async def delete_informe_id(db: Prisma, informe_id: str)-> Informe:
    """ Conseguir a 1 informe de la base de datos segun su id"""
    return await db.informe.delete(where={"id": informe_id})