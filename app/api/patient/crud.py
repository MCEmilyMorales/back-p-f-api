from prisma.models import Paciente
from prisma import Prisma
from datetime import datetime as dt  # Importa correctamente
from app.api.patient.paciente_shema import PacienteCreate

async def create_paciente(db:Prisma, paciente: PacienteCreate) -> Paciente:
    """Permite inserta a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y la fecha de muestra.
    retorna un mensaje de que el paciente fue cargado con exito"""

    await db.paciente.create(
        data=paciente.model_dump()
    )
    return {"Paciente creado con exito"}