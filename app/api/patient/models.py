from pydantic import BaseModel

class PacienteBase(BaseModel):
    nombre: str
    usuario_id: str

class PacienteCreate(PacienteBase):
    pass