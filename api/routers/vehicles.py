from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from ..dependency.dependencies import get_user_validator

router = APIRouter()

# @router.get("/", response_model=list[schemas.Vehicle])
# def read_vehicles(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     current_user: models.Usuario = Depends(get_user_validator),  # Verificar el tipo de usuario
# ):
#     if current_user.tipo != 1:
#         raise HTTPException(status_code=403, detail="Access forbidden: Only employees can access this route.")
    
#     return db.query(models.Vehiculo).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = models.Vehiculo(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/", response_model=list[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Vehiculo).offset(skip).limit(limit).all()

@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.put("/{vehicle_id}", response_model=schemas.Vehicle)
def update_vehicle(vehicle_id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle_data = vehicle.model_dump()
    for key, value in vehicle_data.items():
        setattr(db_vehicle, key, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehiculo).filter(models.Vehiculo.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully"}
