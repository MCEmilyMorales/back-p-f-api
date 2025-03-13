from pydantic import BaseModel, Field
from fastapi import Query
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str = Query(..., min_length=4, max_length=255),
    mail: str = Query(..., regex="@", min_length=6, max_length=50),
    password: str = Query(..., min_length=5, max_length=255)

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioLogin(UsuarioBase):
    nombre:Optional[str] = None
    mail:Optional[str] = None
    password:str = Field(..., min_length=6)

