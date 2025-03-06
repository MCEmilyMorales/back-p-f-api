from prisma.models import Imagen
from prisma import Prisma

async def create_imagen(db: Prisma, ubicacion: str, informe_id: str) -> Imagen:
    """Permite insertar un nuevo usuario en la base de datos.
        Recibe: instancia de base de datos, ubicacion y ID del informe al que pertenece.
        Retorna: objeto Imagen"""
    return await db.imagen.create(data={"ubicacion": ubicacion, "informeId": informe_id})
    
async def get_imagen(db: Prisma, imagen_id: str) -> Imagen | None:
    """ Buscar una imagen por su ID en la base de datos.
        Recibe: instancia de base de datos, ID.
        Retorna: objeto Imagen o None"""
    return await db.imagen.find_unique(where={"id": imagen_id})

async def get_imagenes_by_informe(db: Prisma, informe_id: str) -> list[Imagen]:
    """ Obtener todos las imagenes de un informe en particular.
        Recibe: instancia de base de datos, ID informe.
        Retorna: lista de objetos Imagen.
    """
    return await db.imagen.find_many(where={"informeId": informe_id})

async def delete_imagen(db: Prisma, imagen_id: str) -> bool:
    """Elimina imagen
    Recibe: instancia de base de datos, ID.
    Retorna: True si se elimino, False si no existe.
    """
    imagen = await db.imagen.delete(where={"id": imagen_id})
    return bool(imagen)