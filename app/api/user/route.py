from fastapi import FastAPI, HTTPException, Query
from app.api.database import db
from app.api.user import crud
import uuid

def add_user_routes(app: FastAPI):
    
    @app.post("/users/", tags=["Usuarios"])
    async def create_user(nombre: str = Query(..., min_length=4, max_length=255),
    mail: str = Query(..., regex="@", min_length=6, max_length=50),
    password: str = Query(..., min_length=5, max_length=255)):
        """Crear usuario en la base de datos.
        Recibe: nombre y contraseña.
        Retorna: mensaje con id del usuario creado. 
        """
        new_user = await crud.create_user(db, nombre, mail, password)
        return {"usuario creado con id = ": new_user.id}

    @app.put("/users/{user_id}", tags=["Usuarios"])
    async def update_email(user_id: str, mail: str = Query(..., regex="@", min_length=6, max_length=50)):
        # Validar si id es UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        mailUpdate = await crud.update_email(db, user_id, mail)
        if not mailUpdate:
            raise HTTPException(status_code=404, detail="No se pudo encontrar el usuario para actualizar el mail")
        return {"Mail actualizado correctamente"}


    @app.get("/users/{user_id}", tags=["Usuarios"])
    async def get_user(user_id: str):
        """Obtener un usuario por ID.
        Recibe: ID del usuario. 
        Retorna: ID y nombre del usuario buscado."""
        # Validar si id es UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        user = await crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"id": user.id, "nombre": user.nombre}


    @app.get("/users/", tags=["Usuarios"])
    async def list_users():
        """ Obtener la lista de usuarios.
        Retorna: lista de diccionarios (ID, nombre)"""
        users = await crud.get_all_users(db)
        return [{"id": u.id, "nombre": u.nombre} for u in users]


    @app.delete("/users/{user_id}", tags=["Usuarios"])
    async def delete_user(user_id: str):
        """ Eliminar un usuario.
        Recibe: id del usuario a eliminar. 
        Retorna: mensaje que notifica si se elimina"""
        # Validar si informe_id es UUID
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="ID invalido, debe tener 36 caracteres.")
        deleted = await crud.delete_user(db, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario eliminado"}