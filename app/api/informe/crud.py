from prisma.models import Informe
from prisma import Prisma
from datetime import datetime
from app.api.patient import crud
from fastapi import HTTPException
from app.api.informe.models import InformeCreate


async def create_informe(db: Prisma, informeCreate: InformeCreate) -> Informe:
    """
    Inserta un nuevo informe de un paciente en la base de datos.    
    Recibe: 
    - db: instancia de Prisma
    - fecha_de_muestra: Fecha de la muestra en formato string
    - pacienteId: ID del paciente
    - tipo de estudio
    """
     # Convertir la fecha a formato ISO 8601
    fecha_iso = datetime.strptime(informeCreate.fecha_de_muestra, "%Y-%m-%d %H:%M:%S").isoformat() + "Z"

    # verificar si el paciente existe en la BD:
    paciente_existe=await crud.get_paciente_id(db,informeCreate.paciente_id)
    if not paciente_existe:
        return "Paciente no existe."     
    try:
            informe_principal = await db.informe.create(
                data={
                    "fecha_de_muestra": fecha_iso,
                    "pacienteId": informeCreate.paciente_id,
                    "tipo_estudio":informeCreate.tipo_estudio 
                }
            )
            return {"informe": informe_principal}

    except Exception as exception:
            raise HTTPException(status_code=500, detail=f"Error en la creación: {str(exception)}")


async def get_all_informes(db: Prisma):
    """ 
    Conseguir todos los informes de la base de datos.
    Retorna: lista de objetos de informes.
    """
    return await db.informe.find_many()


async def get_informe_id(db: Prisma, informe_id: str)-> Informe:
    """ 
    Conseguir a 1 informe de la base de datos segun su id
    """
    informe = await db.informe.find_unique(where={"id": informe_id})
    if not informe:
        raise HTTPException(status_code=404, detail="Informe no encontrado")
    return informe 


async def list_informes_por_paciente(db:Prisma, paciente_id:str)->list[Informe]:
    """Busca todos los registros en la tabla informe donde el campo pacienteId coincida con el valor de paciente_id. 
    Retorno: Lista de informes asociados al paciente proporcionado. Si no se encuentran, devuelve una lista vacía []."""
    lista_informes = await db.informe.find_many(where={"pacienteId":paciente_id})
    return lista_informes


async def update_promedio(db: Prisma, id: str, promedio_rta_img:str) -> bool:
    """
    Actualiza informacion - promedio para un informe en la base de datos.
    Recibe: instancia de la base de datos, id del informe y nueva info promedio.
    Retorna: True si la actualización fue exitosa, False si el usuario no fue encontrado.
    """
    informe = await db.informe.find_unique(where={"id": id})
    if not informe:
        return False  # informe no encontrado
    await db.informe.update(
        where={"id": id},
        data={"promedio_rta_img": promedio_rta_img}
    )
    return True  # Indica que la actualización fue exitosa


async def delete_informe_id(db: Prisma, informe_id: str)-> Informe:
    """ 
    Eliminar 1 informe de la base de datos segun su id
    retorna: informe
    """
    return await db.informe.delete(where={"id": informe_id})