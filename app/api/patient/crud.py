from prisma.models import Paciente
from prisma import Prisma

async def create_paciente(db:Prisma, nombre:str) -> Paciente:
    """Permite inserta a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y la fecha de muestra.
    retorna un mensaje de que el paciente fue cargado con exito"""

    await db.paciente.create(
        data={"nombre": nombre}
    )
    return {"Paciente creado con exito"}

async def get_all_pacientes(db: Prisma):
    """ Obtener un objeto de pacientes.
    Retorna: lista de diccionarios"""
    return await db.informe.find_many()

async def get_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Obtiene 1 paciente segun su id."""
    return await db.informe.find_unique(where={"id":paciente_id})

async def delete_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Eliminar a 1 paciente segun su id."""
    return await db.informe.delete(where={"id":paciente_id})

