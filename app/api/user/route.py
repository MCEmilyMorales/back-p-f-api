from fastapi import FastAPI, HTTPException, Query, Depends
from app.api.database import db
from app.api.user import crud
from app.api.user.models import UsuarioCreate
from app.api.user.token.decodificar_token import obtener_usuario_actual
from fastapi.security import OAuth2PasswordRequestForm
from app.api.user.models import UsuarioUpdateMail
import uuid

def add_user_routes(app: FastAPI):
    
    @app.post("/users/", tags=["Usuarios"])
    async def create_user(usuarioCreate: UsuarioCreate):
        """Crear usuario en la base de datos.
        Parametro: mail(unico).
        Retorna: mensaje con id del usuario creado."""
        new_user = await crud.create_user(db,  usuarioCreate.mail)
        return {"usuario creado con id = ": new_user.id}

    
    @app.post("/users_login/", tags=["Usuarios"])
    async def login(form_data: OAuth2PasswordRequestForm = Depends()):
        """El usuario podra loguearse de forma manual.
        Parametro: OAuth2PasswordRequestForm de FastAPI. Recibe el email o el nombre y la contraseña.
        Retorna: Token o mensaje para verificar sus datos. """        
        return await crud.login(db, form_data)
        

    @app.put("/users/actualizar_email", tags=["Usuarios"])
    async def update_email(usuarioUpdateMail: UsuarioUpdateMail):
        """Permite actualizar el mail del usuario.
        Parametro: mail, mail_nuevo.
        Retorna: mensaje de exito de actualizacion o mensaje de error."""
        mailUpdate = await crud.update_email(db, usuarioUpdateMail.mail, usuarioUpdateMail.mail_nuevo)
        if not mailUpdate:
            raise HTTPException(status_code=404, detail="No se pudo encontrar el usuario para actualizar el mail")
        return {"Mail actualizado correctamente"}


    @app.get("/users/{mail}", tags=["Usuarios"])
    async def get_mail_user(mail:str):
        """Obtener un ID por mail de usuario.
        Recibe: Mail del usuario. 
        Retorna: ID del usuario buscado o algun mensaje de error"""
        userId = await crud.get_mail_user(db, mail)
        if not userId:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"id": userId}


    @app.get("/users_id/{user_id}", tags=["Usuarios"])
    async def get_user(user_id:str):
        """Obtener un usuario por ID.
        Recibe: ID del usuario. 
        Retorna: ID y nombre del usuario buscado o algun mensaje de error"""
        # Validar si id es UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        user = await crud.get_user(db, user_id)      
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mail": user.mail}


    @app.get("/users/", tags=["Usuarios"])
    async def list_users():
        """ Obtener la lista de usuarios.
        Retorna: lista de diccionarios (ID, nombre)"""
        users = await crud.get_all_users(db)
        return [{"id": u.id,"mail":u.mail} for u in users]


    @app.delete("/users/{user_id}", tags=["Usuarios"])
    async def delete_user(user_id: str):
        """ Eliminar un usuario definitivamente.
        Recibe: id del usuario a eliminar. 
        Retorna: mensaje que notifica si se elimina o mensaje de error"""
        # Validar si informe_id es UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        deleted = await crud.delete_user(db, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado"}