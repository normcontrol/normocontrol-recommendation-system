from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from .schemas import Document
from sqlalchemy.orm import Session
from . import crud
from .database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

recommendation_router = APIRouter(prefix = '', tags = ['Recommendation'])
@recommendation_router.post('/check')
def check(request: Request, document: Document):
    pass

@recommendation_router.get('/get_all_gost_params')
def get_all_gost_params(db: Session = Depends(get_db)):
    return crud.get_all_gost_params(db)

@recommendation_router.get('/get_gost_params/{gost_id}')
def get_gost_params(gost_id: int, db: Session = Depends(get_db)):
    all_gost_params = crud.get_gost_params(db, gost_id=gost_id)
    if all_gost_params is None:
        raise HTTPException(status_code=404, detail="Gost params not found")
    return all_gost_params