from prisma.models import Usuario
from prisma import Prisma

async def create_user(db: Prisma, nombre: str, mail: str, password: str) -> Usuario:
    """Permite insertar un nuevo usuario en la base de datos.
    Recibe: instancia de base de datos, nombre y contraseña.
    Retorna: objeto Usuario"""
    return await db.usuario.create(data={"nombre": nombre, "mail": mail,"password": password})

async def get_user(db: Prisma, user_id: str) -> Usuario | None:
    """ Buscar un usuario por su ID en la base de datos.
    Recibe: instancia de base de datos, ID.
    Retorna: objeto Usuario o None"""
    return await db.usuario.find_unique(where={"id": user_id})

async def get_all_users(db: Prisma):
    """ Obtener todos los usuarios en la base de datos.
    Recibe: instancia de base de datos.
    Retorna: lista de objetos Usuario.
    """
    return await db.usuario.find_many()

async def delete_user(db: Prisma, user_id: str) -> bool:
    """Elimina un usuario
    Recibe: instancia de base de datos, ID.
    Retorna: True si se elimino, False si no existe.
    """
    user = await db.usuario.delete(where={"id": user_id})
    return bool(user)