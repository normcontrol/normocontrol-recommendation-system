from fastapi import FastAPI
from src.api.router import recommendation_router

app = FastAPI(title = 'Recommendation Service')
app.include_router(recommendation_router)
