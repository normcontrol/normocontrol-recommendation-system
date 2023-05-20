from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from .schemas import Document, GostID, OriginDocument
from sqlalchemy.orm import Session
from . import crud
from .database import SessionLocal
from ..system.Checker import Checker

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

recommendation_router = APIRouter(prefix = '', tags = ['Recommendation'])
@recommendation_router.post('/check')
def check(gost_id: GostID, origin_document: OriginDocument, request: Request, document: Document, db: Session = Depends(get_db)):
    origin_document = crud.get_document(db, origin_document.document_id)
    input_document = origin_document.input_document
    checker = Checker(document, gost_id.gost_id, input_document, db)
    document = checker.check()
    if 'odt' in input_document:
        output_document = checker.create_docx_report()
    elif 'pdf' in input_document:
        output_document = checker.create_pdf_report()
    return output_document

@recommendation_router.get('/get_all_gost_params')
def get_all_gost_params(db: Session = Depends(get_db)):
    return crud.get_all_gost_params(db)

@recommendation_router.get('/get_gost_params/{gost_id}')
def get_gost_params(gost_id: int, db: Session = Depends(get_db)):
    all_gost_params = crud.get_gost_params(db, gost_id=gost_id)
    if all_gost_params is None:
        raise HTTPException(status_code=404, detail="Gost params not found")
    return all_gost_params