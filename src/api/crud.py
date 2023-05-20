from sqlalchemy.orm import Session
from . import models

def get_all_gost_params(db: Session):
    return db.query(models.Gost_params).all()

def get_gost_params(db: Session, gost_id: int):
    return db.query(models.Gost_params).filter(models.Gost_params.id_gost == gost_id).all()

def get_document(db: Session, document_id: int):
    return db.query(models.Documents).filter(models.Documents.id_document == document_id).first()
# def get_document_statistics(db: Session, document_id: int):
#     return db.query(models.DocumentStatistics).get(models.DocumentStatistics.id_document == document_id)