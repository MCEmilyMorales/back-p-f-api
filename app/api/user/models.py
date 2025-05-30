from pydantic import BaseModel, Field, EmailStr, field_validator
import re
import uuid

class UsuarioBase(BaseModel):
    mail: EmailStr

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdateMail(UsuarioBase):
    mail: EmailStr
    mail_nuevo: EmailStr
    


