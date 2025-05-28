from prisma.models import Paciente
from prisma import Prisma
from app.api.patient.models import PacienteCreate
from fastapi import HTTPException, Query
from prisma.errors import PrismaError
from typing import Optional
from datetime import datetime

async def create_paciente(db:Prisma, paciente: PacienteCreate, usuarioId:str ) -> Paciente | None:
    """Permite insertar a un nuevo paciente en la base de datos.
    Recibe: instancia de base de datos, nombre y id del medico (usuario).
    retorna un mensaje de que el paciente fue cargado con exito"""
    await db.paciente.create(
        data={"nombre": paciente.nombre, 
              "dni": paciente.dni,
              "sexo": paciente.sexo,
              "fecha_de_nacimiento":paciente.fecha_de_nacimiento,
              "usuarioId":usuarioId}
    )
    return {"Paciente creado con exito"}


async def get_all_pacientes(db: Prisma):
    """ Obtener un objeto de pacientes.
    Retorna: lista de diccionarios"""
    return await db.paciente.find_many()


async def get_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Obtiene 1 paciente segun su id. 
    Recibe: instancia de base de datos, id del paciente.
    retorna al paciente o None"""
    return await db.paciente.find_unique(where={"id":paciente_id})


async def list_paciente_por_doctor(db:Prisma, user_id:str)->list[Paciente]:
    """Busca todos los registros en la tabla paciente donde el campo usuarioId coincida con el valor de user_id. 
    Retorno: La función retorna la lista de pacientes asociados al usuario proporcionado. Si no se encuentran pacientes, devuelve una lista vacía []."""
    lista_paciente= await db.paciente.find_many(where={"usuarioId":user_id})
    return lista_paciente


async def delete_paciente_id(db: Prisma, paciente_id: str)-> Paciente | None:
    """ Eliminar a 1 paciente segun su id.
    Recibe: instancia de base de datos, id del paciente.
    retorna al paciente o None"""
    await db.imagen.delete_many(where={"informe": {"pacienteId": paciente_id}})
    await db.informe.delete_many(where={"pacienteId": paciente_id})
    return await db.paciente.delete(where={"id":paciente_id})

#conseguir paciente por dni: get_paciente_dni
async def get_paciente_dni(db: Prisma, paciente_dni: str)-> Paciente:
    """ Obtiene 1 paciente segun su dni. 
    Recibe: instancia de base de datos, dni del paciente.
    retorna al paciente o status_code"""
    try: 
        paciente=await db.paciente.find_many(where={"dni":paciente_dni })
        if not paciente:
            raise HTTPException(status_code=404, detail='Paciente con Dni no encontrado')
        return paciente
    except PrismaError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")


# conseguir paciente segun su dni y sexo
async def get_paciente_dni_sexo(db: Prisma, paciente_dni: str, paciente_sexo: Optional[str])-> Paciente:
    """ Obtiene 1 paciente segun su dni y sexo. 
    Recibe: instancia de base de datos, dni del paciente y sexo del paciente.
    retorna al paciente o status_code"""
    try: 
        paciente=await db.paciente.find_many(where={"dni":paciente_dni, "sexo":paciente_sexo })
        if not paciente:
            raise HTTPException(status_code=404, detail='Paciente con Dni no encontrado')
        return paciente
    except PrismaError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")


# conseguir paciente segun su fecha de nacimiento
async def get_paciente_fecha_de_nacimiento(db: Prisma,  paciente_dni: str, paciente_sexo: Optional[str], paciente_fecha_de_nacimiento:str)-> Paciente:
    """ Obtiene 1 paciente segun su fecha de nacimiento. 
    Recibe: instancia de base de datos, fecha de nacimiento del paciente.
    retorna al paciente o status_code"""
    try: 
        paciente=await db.paciente.find_many(where={"dni":paciente_dni, "sexo":paciente_sexo ,"fecha_de_nacimiento":paciente_fecha_de_nacimiento })
        if not paciente:
            raise HTTPException(status_code=404, detail='Paciente no encontrado')
        return paciente
    except PrismaError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")


def validar_dni(paciente_dni: str= Query(...)) -> str: 
    if not paciente_dni.isdigit() or (len(paciente_dni) not in(7, 8)):
        raise HTTPException(status_code=400, detail="El DNI debe tener exactamente 7 u 8 dígitos numéricos.")
    return paciente_dni


def validar_sexo(paciente_sexo:  Optional[str] = Query(None)) -> Optional[str]:
    if paciente_sexo and paciente_sexo not in("F", "M"):
        raise HTTPException(status_code=400, detail="El SEXO debe ser 'M' para masculino o 'F' para femenino.")
    return paciente_sexo


def validar_fecha_de_nacimiento(paciente_fecha_de_nacimiento:  Optional[str] = Query(None)) -> Optional[str]:
    if paciente_fecha_de_nacimiento:
        try:
            # Intenta parsear la fecha con el formato YYYY-MM-DD
            datetime.strptime(paciente_fecha_de_nacimiento, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="La fecha de nacimiento debe tener el formato 'YYYY-MM-DD'"
            )
    return paciente_fecha_de_nacimiento