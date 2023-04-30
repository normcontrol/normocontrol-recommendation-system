from fastapi import APIRouter
from starlette.requests import Request
from schemas import Document

recommendation_router = APIRouter(prefix = '', tags = 'Recommendation')
@recommendation_router.post('/check')
def check(request: Request, document: Document):
    pass