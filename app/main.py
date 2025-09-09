from fastapi import FastAPI
from sqlmodel import Session
from sqlalchemy import text
from app.database.database import engine

from app.routes.users.UsersRoutes import router as users_router

app = FastAPI()



@app.on_event("startup")
def test_db():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1")) 
        print("Conexión a la base de datos exitosa")
    except Exception as e:
        print("❌ Error al conectar:", e)

# Routers
app.include_router(users_router, prefix="/users", tags=["Users"])


# Ruta raíz 
@app.get("/")
def root():
    return {"msg": "Bienvenido a DocsFlow API 🚀"}