from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.api import secret

SQL_DATABASE_URL = f"mysql://{secret.USER_LOGIN}:{secret.USER_PASSWORD}@{secret.DB_IP}:{secret.DB_PORT}/normcontrol.ru"
engine = create_engine(
    SQL_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()