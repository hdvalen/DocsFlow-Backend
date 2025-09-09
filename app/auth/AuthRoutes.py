from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from app.database.database import get_db
from app.auth.AuthJwtHandler import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginSchema(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    # Traemos al usuario como diccionario
    db_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().fetchone()

    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # Verificar la contraseña usando el hash guardado
    if not pwd_context.verify(user.password, db_user["password_hash"]):
       raise HTTPException(status_code=401, detail="Credenciales inválidas")


    # Buscar el rol del usuario
    role_row = db.execute(
        text("""
            SELECT r.name FROM roles r
            JOIN user_roles ur ON ur.role_id = r.id
            WHERE ur.user_id = :user_id
        """),
        {"user_id": db_user["id"]}
    ).mappings().fetchone()

    role = role_row["name"] if role_row else "user"

    # Crear token con rol
    token = create_access_token({"sub": db_user["email"], "role": role})

    return {"access_token": token, "token_type": "bearer"}
