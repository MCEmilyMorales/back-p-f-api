from prisma.models import Usuario
from prisma import Prisma
import bcrypt
from fastapi import HTTPException


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


async def login(db: Prisma,usuario_login):
     # el usuario existe???
    if not usuario_login.mail and not usuario_login.nombre:
        raise HTTPException(status_code=400, detail='Debes proporcionar un mail o un nombre')
    
    user = None
    if usuario_login.mail:
        user = await get_user_email(db,usuario_login.mail) 
    elif usuario_login.nombre:
        user = await get_user_nombre(db, usuario_login.nombre) 
    
    if not user:
        raise HTTPException(status_code=400, detail='Usuario no encontrado')
 # Verificar si el usuario existe y si la contraseña es correcta
    
    if not await verificar_password(usuario_login.password, user.password):
        raise HTTPException(status_code=400, detail='Contraseña incorrecta')

    return {"message": "Login exitoso"}

async def hashear_password(password:str)->str:
    """Hashea la contraseña de forma segura"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')  
    return hashed_password


async def verificar_password(password: str, passwordBD: str) -> bool:
    """Compara la contraseña ingresada con la almacenada en la base de datos."""
    try:
        # Verifica que las contraseñas sean iguales usando bcrypt
        compare = bcrypt.checkpw(password.encode('utf-8'), passwordBD.encode('utf-8'))
        return compare
    except Exception as e:
        print(f"Error al verificar la contraseña: {e}")
        return False
    

async def get_user_email(db: Prisma, mail: str)-> Usuario:
    """Obtiene un usuario por su email"""
    return await db.usuario.find_unique(where={"mail": mail})


async def get_user_nombre(db: Prisma, nombre: str)-> Usuario:
    """Obtiene un usuario por su email"""
    return await db.usuario.find_unique(where={"nombre": nombre})


async def update_email(db: Prisma, user_id: str, mail:str) -> bool:
    """Permite actualizar el mail del usuario en la base de datos.
    Recibe: instancia de base de datos, id y nuevo mail.
    Retorna: true si se actualizo y false si el usuario con ese id no fue encontrado"""
    user=await db.usuario.find_unique(where={"id": user_id})
    if not user:
        return False  # Usuario no encontrado
    await db.usuario.update(
        where={"id": user_id},
        data={"mail": mail}
    )
    return True  # Indica que la actualización fue exitosa
