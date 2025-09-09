# app/config.py
from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

class Settings:
    
    # DB (si quieres centralizarla también aquí)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "DocsFlow")

# JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")  
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
