from prisma.models import Paciente
from prisma import Prisma

async def create_paciente(db:Prisma, nombre:str, usuarioId:str) -> Paciente | None:
    """Permite inserta a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y la fecha de muestra.
    retorna un mensaje de que el paciente fue cargado con exito"""
    user=await db.usuario.find_unique(where={"id": usuarioId})
    if not user:
        return None  # Usuario no encontrado
    await db.paciente.create(
        data={"nombre": nombre, "usuarioId":usuarioId}
    )
    return {"Paciente creado con exito"}

async def get_all_pacientes(db: Prisma):
    """ Obtener un objeto de pacientes.
    Retorna: lista de diccionarios"""
    return await db.paciente.find_many()

async def get_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Obtiene 1 paciente segun su id."""
    return await db.paciente.find_unique(where={"id":paciente_id})

async def list_paciente_por_doctor(db:Prisma, user_id:str)->list[Paciente]:
    """Busca todos los registros en la tabla paciente donde el campo usuarioId coincida con el valor de user_id. 
    Retorno: La función retorna la lista de pacientes asociados al usuario proporcionado. Si no se encuentran pacientes, devuelve una lista vacía []."""
    lista_paciente= await db.paciente.find_many(where={"usuarioId":user_id})
    return lista_paciente

async def delete_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Eliminar a 1 paciente segun su id."""
    await db.imagen.delete_many(where={"informe": {"pacienteId": paciente_id}})
    await db.informe.delete_many(where={"pacienteId": paciente_id})
    return await db.paciente.delete(where={"id":paciente_id})

