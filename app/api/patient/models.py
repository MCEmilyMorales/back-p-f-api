from pydantic import BaseModel

class PacienteBase(BaseModel):
    nombre: str
    num_historia_clinica: str
    usuario_id: str

class PacienteCreate(PacienteBase):
    pass