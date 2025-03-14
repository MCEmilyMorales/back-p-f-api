from pydantic import BaseModel

class PacienteBase(BaseModel):
    nombre: str
    num_historia_clinica: str
    usuarioId: str

class PacienteCreate(PacienteBase):
    pass