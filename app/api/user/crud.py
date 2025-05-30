from prisma.models import Usuario
from prisma import Prisma
import bcrypt
from fastapi import HTTPException
from app.api.user.token import crear_token
from dotenv import load_dotenv
import os
from datetime import timedelta

# Cargar variables desde .env
load_dotenv()


async def create_user(db: Prisma,  mail: str) -> Usuario:
    """Crea un nuevo usuario en la base de datos.
    Parametros: instancia de la base de datos, nombre, correo electrónico y contraseña en texto plano (se debe hashear antes de almacenarla).
    Retorna: objeto del usuario creado."""

    existing_user = await db.usuario.find_unique(where={"mail": mail})
    if existing_user:
        raise HTTPException(status_code=409, detail="El correo ya está registrado.")
    return await db.usuario.create(data={"mail": mail})

async def get_user(db: Prisma, user_id: str) -> Usuario | None:
    """ Buscar un usuario por su ID en la base de datos.
    Parametros: instancia de la base de datos, ID del usuario.
    Retorna: Usuario si existe, None si no se encuentra."""
    user=await db.usuario.find_unique(where={"id": user_id})
    return user

async def get_mail_user(db: Prisma, mail: str) -> Usuario | None:
    """ Buscar un usuario por su mail en la base de datos.
    Parametros: instancia de la base de datos, mail del usuario.
    Retorna: Usuario si existe, None si no se encuentra."""
    user = await db.usuario.find_unique(where={"mail": mail})
    return user.id


async def get_all_users(db: Prisma)-> list[Usuario]:
    """ Obtiene todos los usuarios en la base de datos.
    Parametros: instancia de la base de datos.
    Retorna: Lista de usuarios."""
    return await db.usuario.find_many()


async def delete_user(db: Prisma, user_id: str) -> bool:
    """Elimina un usuario por su ID.
    Parametros: instancia de la base de datos, ID del usuario a eliminar.
    Retorna: True si se eliminó correctamente, False si el usuario no existe."""
    user = await db.usuario.delete(where={"id": user_id})
    return bool(user)


async def login(db: Prisma,form_data)-> dict:
    """Autentica a un usuario y genera un token JWT.
    Parametros: instancia de la base de datos, datos de autenticación con nombre de usuario o correo y contraseña.
    Retorna: Token de acceso y tipo de token;
            Si las credenciales no son correctas lanza HTTPException: Si las credenciales son incorrectas."""
    username = form_data.username
    
    if '@' in username:
        user =  await get_user_email(db, form_data.username)
    else:
        user = await get_user_nombre(db, form_data.username)
    
    if not user or not await verificar_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail='Verifique sus datos.')
    # Generar token de acceso
    token_de_acceso = crear_token.crear_access_token(
        data={'sub': user.id},
        expiracion=timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    )
    
    return {'access_token': token_de_acceso, 'token_type': 'bearer'}

async def hashear_password(password:str)->str:
    """Hashea la contraseña de forma segura usando bcrypt.
    Parametros: contraseña en texto plano.
    Retorna: contraseña hasheada."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')  
    return hashed_password


async def verificar_password(password: str, passwordBD: str) -> bool:
    """Compara una contraseña ingresada con la almacenada en la base de datos.
    Parametros: Contraseña ingresada por el usuario. Contraseña almacenada en la base de datos (hasheada).
    Retorna: True si la contraseña es la correcta, False si no lo es."""
    try:
        # Verifica que las contraseñas sean iguales usando bcrypt
        compare = bcrypt.checkpw(password.encode('utf-8'), passwordBD.encode('utf-8'))
        return compare
    except Exception as e:
        print(f"Error al verificar la contraseña: {e}")
        return False
    

async def get_user_email(db: Prisma, mail: str)-> Usuario:
    """Obtiene un usuario por su email.
    Parametro: instancia de la base de datos, mail del usuario..
    Retorna: Usuario si existe, None si no se encuentra."""
    return await db.usuario.find_unique(where={"mail": mail})


async def get_user_nombre(db: Prisma, nombre: str)-> Usuario:
    """Obtiene un usuario por su nombre.
    Parametro: instancia de la base de datos, nombre del usuario.
    Retorna: Usuario si existe, None si no se encuentra."""
    return await db.usuario.find_unique(where={"nombre": nombre})


async def update_email(db: Prisma, mail: str, mail_nuevo: str) -> bool:
    """Actualiza el mail de un usuario en la base de datos."""
    user = await db.usuario.find_first(where={"mail": mail})
    if not user:
        print(f"Usuario no encontrado.{user}")
        return False  # No se encontró el usuario

    await db.usuario.update(
        where={"mail": mail},
        data={"mail": mail_nuevo}
    )
    return True
