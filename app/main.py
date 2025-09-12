from fastapi import FastAPI, Depends
from sqlmodel import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.routes.users.UsersRoutes import router as users_router
from app.auth.AuthRoutes import router as auth_router
from app.auth.dependencies import JWTBearer
from app.routes.documentPdf.DocumentRouter import router as document_router
from app.routes.email.emailRouter import router as email_router

app = FastAPI()

# 🔹 Configuración de CORS
origins = [
    "http://localhost:5173",  
    "http://localhost:5174",  
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],     
)

@app.on_event("startup")
def test_db():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa")
    except Exception as e:
        print("❌ Error al conectar:", e)

# 🔹 Routers combinados
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router)  
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(email_router, prefix="/email", tags=["Email"])  

# 🔹 Ruta raíz
@app.get("/")
def root():
    return {"msg": "Bienvenido a DocsFlow API 🚀"}
