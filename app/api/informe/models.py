from typing import Any, Dict
from pydantic import BaseModel

class InformeBase(BaseModel):
    fecha_de_muestra: str
    paciente_id: str
    tipo_estudio: str

class InformeCreate(InformeBase):
    pass  # Si no hay cambios, hereda todo de InformeBase

class InformeResponse(InformeBase):
    id: str

    class Config:
        from_attributes = True  # Permite convertir desde modelos de BD

class InformeUpdatePromedio(BaseModel):
    id: str
    promedio_rta_img: str