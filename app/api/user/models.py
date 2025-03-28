from pydantic import BaseModel, Field, EmailStr, field_validator
import re
import uuid

class UsuarioBase(BaseModel):
    nombre: str = Field(exclude=True, min_length=2, max_length=50)
    @field_validator('nombre', mode='after')
    @classmethod
    def es_invalido(cls, value: str) -> str:
        if not value or value[0].isdigit():
            raise ValueError('El nombre no puede iniciar con un numero.')
        return value
    
    mail: EmailStr
    
    password: str = Field(exclude=True, min_length=5, max_length=80)
    @field_validator('password', mode='after')
    @classmethod
    def es_valido(cls, value:str) -> str:
        pattern=r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
        if not re.match(pattern, value):
            raise ValueError('La password debe contener al menos 1 numero, 1 minuscula, 1 MAYUSCULA, 1 simbolo(@$!%*?&)')
        return value
    

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdateMail(UsuarioBase):
    user_id:str = uuid.UUID
    mail: EmailStr
    nombre: str = Field(default=None, exclude=True)
    password: str = Field(default=None, exclude=True)


