from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.orm import Session
from database import get_db
from models import UsuarioBase
from ..dependency.dependencies import get_user_validator
router = APIRouter()

# @router.get("/", response_model=list[UsuarioBase])
# def read_empleados(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     current_user: UsuarioBase = Depends(get_user_validator(1))
# ):
#     return db.query(UsuarioBase).filter(UsuarioBase.tipo == 1).offset(skip).limit(limit).all()

# Crear un nuevo empleado (tipo = 1)
@router.post("/", response_model=schemas.Usuario)
def create_empleado(empleado: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_empleado = models.Usuario(**empleado.model_dump())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado

# Obtener todos los empleados (tipo = 1)
@router.get("/", response_model=list[schemas.Usuario])
def read_empleados(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.tipo == 1).offset(skip).limit(limit).all()

# Obtener un empleado por ID
@router.get("/{empleado_id}", response_model=schemas.Usuario)
def read_empleado(empleado_id: int, db: Session = Depends(get_db)):
    db_empleado = db.query(models.Usuario).filter(models.Usuario.id == empleado_id, models.Usuario.tipo == 1).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_empleado

# Actualizar un empleado
@router.put("/{empleado_id}", response_model=schemas.Usuario)
def update_empleado(empleado_id: int, empleado: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_empleado = db.query(models.Usuario).filter(models.Usuario.id == empleado_id, models.Usuario.tipo == 1).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    for key, value in empleado.model_dump(exclude_unset=True).items():
        setattr(db_empleado, key, value)

    db.commit()
    db.refresh(db_empleado)
    return db_empleado

# Eliminar un empleado
@router.delete("/{empleado_id}")
def delete_empleado(empleado_id: int, db: Session = Depends(get_db)):
    db_empleado = db.query(models.Usuario).filter(models.Usuario.id == empleado_id, models.Usuario.tipo == 1).first()
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(db_empleado)
    db.commit()
    return {"message": "Empleado eliminado exitosamente"}
