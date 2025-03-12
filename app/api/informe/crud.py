from prisma.models import Informe
from prisma import Prisma
from typing import List
from datetime import datetime
from app.api.patient import crud
from fastapi import HTTPException
from app.api.informe.models import InformeCreate

async def create_informe(db: Prisma, informeCreate: InformeCreate) -> Informe:
    """Inserta un nuevo informe de un paciente en la base de datos.    
    Recibe: 
    - db: instancia de Prisma
    - fecha_de_muestra: Fecha de la muestra en formato string
    - pacienteId: ID del paciente
    - imagenes: Lista de IDs de imágenes a conectar
    """
     # Convertir la fecha a formato ISO 8601
    fecha_iso = datetime.strptime(informeCreate.fecha_de_muestra, "%Y-%m-%d").isoformat() + "Z"

    # verificar si el paciente existe en la BD-
    paciente_existe=await crud.get_paciente_id(db,informeCreate.paciente_id)
    if not paciente_existe:
        return "Paciente no existe."  # Paciente no encontrado         
    try:
            # 1. Crear el informe sin conectar las imágenes
            informe_principal = await db.informe.create(
                data={
                    "fecha_de_muestra": fecha_iso,
                    "pacienteId": informeCreate.paciente_id,
                    "numero_informe": informeCreate.numero_informe,
                    "tipo_estudio":informeCreate.tipo_estudio 
                }
            )
            return {"informe": informe_principal}

    except Exception as exception:
            raise HTTPException(status_code=500, detail=f"Error en la creación: {str(exception)}")

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