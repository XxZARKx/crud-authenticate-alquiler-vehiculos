from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from models import UsuarioBase
from ..dependency.dependencies import get_user_validator
router = APIRouter()


# @router.get("/", response_model=list[UsuarioBase])
# def read_clientes(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     current_user: UsuarioBase = Depends(get_user_validator(2))  # Solo tipo 2
# ):
#     return db.query(UsuarioBase).filter(UsuarioBase.tipo == 2).offset(skip).limit(limit).all()

# Crear un nuevo cliente (tipo = 2)
@router.post("/", response_model=schemas.Usuario)
def create_cliente(cliente: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_cliente = models.Usuario(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Obtener todos los clientes (tipo = 2)
@router.get("/", response_model=list[schemas.Usuario])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Usuario).filter(models.Usuario.tipo == 2).offset(skip).limit(limit).all()

# Obtener un cliente por ID
@router.get("/{cliente_id}", response_model=schemas.Usuario)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Usuario).filter(models.Usuario.id == cliente_id, models.Usuario.tipo == 2).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# Actualizar un cliente
@router.put("/{cliente_id}", response_model=schemas.Usuario)
def update_cliente(cliente_id: int, cliente: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Usuario).filter(models.Usuario.id == cliente_id, models.Usuario.tipo == 2).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Eliminar un cliente
@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Usuario).filter(models.Usuario.id == cliente_id, models.Usuario.tipo == 2).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"message": "Cliente eliminado exitosamente"}
