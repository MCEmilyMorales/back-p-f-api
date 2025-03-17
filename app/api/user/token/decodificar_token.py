from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users_login')#! controlar esto

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = payload.get("sub")
        # role: str = payload.get("role")
        if username is None :#or role is None(se agregara cuando se cree mas de un rol)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return {"username": username}# "role": role(se agregara cuando se cree mas de un rol)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    

