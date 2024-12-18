from fastapi import APIRouter, Depends
from api.dependency.dependencies import get_user_validator
from models import UsuarioBase

router = APIRouter()

@router.get("/protected")
def get_protected_data(current_user: UsuarioBase = Depends(get_user_validator(1))):
    return {"user": current_user}