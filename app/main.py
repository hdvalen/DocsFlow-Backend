from fastapi import FastAPI
from sqlmodel import Session
from sqlalchemy import text
from app.database.database import engine

app = FastAPI()

@app.on_event("startup")
def test_db():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1")) 
        print("Conexión a la base de datos exitosa")
    except Exception as e:
        print("❌ Error al conectar:", e)
