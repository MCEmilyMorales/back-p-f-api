from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()


def crear_access_token(data:dict, expiracion:timedelta):
    """"""
    vencio=datetime.now(timezone.utc) + expiracion  # ✅ Usamos now(timezone.utc)Siempre en UTC
    data["exp"] = vencio.timestamp()  # Guardar como timestamp (segundos desde 1970)
    return jwt.encode(data, os.getenv('SECRET_KEY'),algorithm=os.getenv('ALGORITHM'))

