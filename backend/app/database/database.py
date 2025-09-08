from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
from sqlmodel import create_engine
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
if not all([DB_USER, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Variables de entorno de la base de datos incompletas")

urlConection = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(urlConection)

def get_db():
    with Session(engine) as session:
        yield session
