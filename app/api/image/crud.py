from fastapi import HTTPException
from prisma.models import Imagen
from prisma import Prisma
import bcrypt
from datetime import datetime


async def create_imagen(db: Prisma, ubicacion: str, informe_id: str) -> Imagen:
    """ 
    Permite insertar una nueva imagen en la base de datos.
    Recibe: instancia de base de datos, ubicacion y ID del informe al que pertenece.
    Retorna: objeto Imagen
    """
    return await db.imagen.create(data={"ubicacion": ubicacion, "informeId": informe_id})


async def get_ubicacion_imagen(db: Prisma, imagen_id: str) -> str | None:
    """ 
    Buscar una imagen por su ID en la base de datos.
    Recibe: instancia de base de datos, ID.
    Retorna: ubicacion (string) o None
    """
    imagen = await db.imagen.find_unique(where={"id": imagen_id})
    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    else:
        return imagen.ubicacion
    
    
async def get_imagen(db: Prisma, imagen_id: str) -> Imagen | None:
    """ 
    Buscar una imagen por su ID en la base de datos.
    Recibe: instancia de base de datos, ID.
    Retorna: objeto Imagen o None
    """
    return await db.imagen.find_unique(where={"id": imagen_id})


async def get_imagenes_by_informe(db: Prisma, informe_id: str) -> list[Imagen]:
    """ 
    Obtener todos las imagenes de un informe en particular.
    Recibe: instancia de base de datos, ID informe.
    Retorna: lista de objetos Imagen.
    """
    return await db.imagen.find_many(where={"informeId": informe_id})


async def delete_imagen(db: Prisma, imagen_id: str) -> bool:
    """
    Elimina imagen.
    Recibe: instancia de base de datos, ID de la imagen.
    Retorna: True si se elimino, False si no existe.
    """
    imagen = await db.imagen.delete(where={"id": imagen_id})
    return bool(imagen)


async def get_paciente_by_image(db: Prisma, informe_id: str) -> str:
    """ 
    Obtener el nombre del paciente relacionado a una imagen.
    Recibe: instancia de base de datos, ID informe.
    Retorna: el nombre del paciente.
    """
    informe = await db.informe.find_unique(where={"id": informe_id})
    paciente= await db.paciente.find_unique(where={"id": informe.pacienteId})
    return paciente.nombre


async def generar_nombre_archivo(db: Prisma, informe_id) -> str:
    """ 
    Obtener nombre para imagen que contega el nombre del paciente asociado, hash y fecha.
    Recibe: instancia de base de datos, ID informe.
    Retorna: nombre para la imagen.
    """
    nombrePaciente= await get_paciente_by_image(db, informe_id)

    hash_bytes = bcrypt.hashpw(nombrePaciente.encode(), bcrypt.gensalt())
    hash_base64 = hash_bytes.decode()[-8:]
    hash_base64=hash_base64.replace('/', '-')
    fecha_actual = datetime.now().strftime("%Y%m%d")

    return f"{nombrePaciente}_{hash_base64}_{fecha_actual}"
