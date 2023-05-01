from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from .schemas import Document
from sqlalchemy.orm import Session
from . import crud
from .database import SessionLocal
from ..system.Rule import Rule

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

recommendation_router = APIRouter(prefix = '', tags = ['Recommendation'])
@recommendation_router.post('/check')
def check(gost_id: int, request: Request, document: Document, db: Session = Depends(get_db)):
    rules_list = []
    all_gost_params = crud.get_gost_params(db, gost_id=gost_id)
    if all_gost_params is None:
        raise HTTPException(status_code=404, detail="Gost params not found!")
    for param in all_gost_params:
        rules_list.append(Rule(param.id_elements.description, param.id_elements.element,
                               param.id_params.param, param.is_recommented, param.operator, param.value))

    for element in document.content.values():
        element.result = {}
        for rule in rules_list:
            if rule.structural_element == element.current_element_mark:
                match rule.operator:
                    case '=':
                        if element.dict()[rule.parameter] == rule.value:
                            element.result[rule.parameter] = "OK!"
                        else:
                            if rule.is_recommend:
                                element.result[rule.parameter] = "Warning!"  # TODO Exceptions
                            else:
                                element.result[rule.parameter] = "Error!"  # TODO Exceptions
                    case '>=':
                        if element.dict()[rule.parameter] >= float(rule.value):
                            element.result[rule.parameter] = "OK!"
                        else:
                            if rule.is_recommend:
                                element.result[rule.parameter] = "Warning!"  # TODO Exceptions
                            else:
                                element.result[rule.parameter] = "Error!"  # TODO Exceptions
                    case '<=':
                        if element.dict()[rule.parameter] <= float(rule.value):
                            element.result[rule.parameter] = "OK!"
                        else:
                            if rule.is_recommend:
                                element.result[rule.parameter] = "Warning!"  # TODO Exceptions
                            else:
                                element.result[rule.parameter] = "Error!"  # TODO Exceptions
    return document

@recommendation_router.get('/get_all_gost_params')
def get_all_gost_params(db: Session = Depends(get_db)):
    return crud.get_all_gost_params(db)

@recommendation_router.get('/get_gost_params/{gost_id}')
def get_gost_params(gost_id: int, db: Session = Depends(get_db)):
    all_gost_params = crud.get_gost_params(db, gost_id=gost_id)
    if all_gost_params is None:
        raise HTTPException(status_code=404, detail="Gost params not found")
    return all_gost_params