from prisma.models import Informe
from prisma import Prisma
from typing import List
from datetime import datetime
from app.api.image import crud
from fastapi import HTTPException

async def create_informe(db: Prisma, fecha_de_muestra:str, pacienteId:str,imagenes: List[str]) -> Informe:
    """Inserta un nuevo informe de un paciente en la base de datos.    
    Recibe: 
    - db: instancia de Prisma
    - fecha_de_muestra: Fecha de la muestra en formato string
    - pacienteId: ID del paciente
    - imagenes: Lista de IDs de imágenes a conectar
    """
     # Convertir la fecha a formato ISO 8601
    fecha_iso = datetime.fromisoformat(fecha_de_muestra).isoformat()
    try:
            # 1. Crear el informe sin conectar las imágenes
            informe_principal = await db.informe.create(
                data={
                    "fecha_de_muestra": fecha_iso,
                    "pacienteId": pacienteId,
                    "status": "pendiente"  # Estado inicial
                }
            )

            # 2. Llamar al método de creación de imágenes
            exito = await crud.create_imagen(informe_id=informe_principal.id)
            if not exito:
                raise HTTPException(status_code=400, detail="Error en el proceso secundario")

            # 3. Si el proceso de imágenes fue exitoso, actualizar el informe
            actualizar_registro = await db.informe.update(
                where={"id": informe_principal.id},
                data={
                    "status": "completo",
                    "imagenes": {"connect": [{"id": img_id} for img_id in imagenes]}
                }
            )

            return {"message": "Informe creado con éxito", "informe_id": actualizar_registro.id}

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