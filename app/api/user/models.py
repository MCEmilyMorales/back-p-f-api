from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional
import uuid

class UsuarioBase(BaseModel):
    nombre: str #= Field(..., min_length=4, max_length=255),
    mail: str #= EmailStr,
    password: str #= constr(min_length=5, max_length=255, pattern=r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$")

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdateMail(UsuarioBase):
    id:str#: uuid.UUID
    mail:str#: EmailStr


