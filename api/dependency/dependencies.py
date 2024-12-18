from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Callable

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_validator(tipo_requerido: int) -> Callable:
    async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ) -> Usuario:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )
            
            usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
            if usuario is None or usuario.tipo != tipo_requerido:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para acceder a este recurso"
                )
            return usuario
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    return get_current_user