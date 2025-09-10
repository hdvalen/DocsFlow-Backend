from fastapi import FastAPI, Depends
from sqlmodel import Session
from sqlalchemy import text
from app.database.database import engine
from app.routes.users.UsersRoutes import router as users_router
from app.auth.AuthRoutes import router as auth_router
from app.auth.dependencies import JWTBearer

app = FastAPI()

@app.on_event("startup")
def test_db():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        print("Conexión a la base de datos exitosa")
    except Exception as e:
        print("❌ Error al conectar:", e)

app.include_router(users_router)
app.include_router(auth_router)

@app.get("/dashboard", dependencies=[Depends(JWTBearer())])
async def dashboard():
    return {"message": "Bienvenido, estás autenticado"}

@app.get("/")
def root():
    return {"msg": "Bienvenido a DocsFlow API 🚀"}
