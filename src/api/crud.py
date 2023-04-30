from sqlalchemy.orm import Session
from . import models

def get_all_gost_params(db: Session):
    return db.query(models.Gost_params).all()

def get_gost_params(db: Session, gost_id: int):
    return db.query(models.Gost_params).filter(models.Gost_params.id_gost == gost_id).all()