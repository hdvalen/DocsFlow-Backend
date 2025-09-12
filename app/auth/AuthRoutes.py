from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from pydantic import BaseModel
from app.database.database import get_db
from app.core.security import create_access_token
from app.schemas.Users.UsersSchema import UserResponse, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_ATTEMPTS = 5
LOCK_TIME_MINUTES = 30

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=LoginResponse)
def login(user: LoginSchema, db: Session = Depends(get_db)):
    # 1️⃣ Buscar usuario
    db_user = db.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {"email": user.email}
    ).mappings().fetchone()

    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    # 2️⃣ Obtener rol del usuario
    role_row = db.execute(
        text("""
            SELECT r.name 
            FROM roles r
            JOIN user_roles ur ON ur.role_id = r.id
            WHERE ur.user_id = :user_id
        """),
        {"user_id": db_user["id"]}
    ).mappings().fetchone()
    role = role_row["name"] if role_row else "user"

    # 3️⃣ Verificar si está bloqueado (solo usuarios normales, no admin)
    if role != "admin" and db_user["failed_attempts"] >= MAX_ATTEMPTS:
        last_update = db_user["updated_at"]
        if last_update and (datetime.utcnow() - last_update) < timedelta(minutes=LOCK_TIME_MINUTES):
            remaining = timedelta(minutes=LOCK_TIME_MINUTES) - (datetime.utcnow() - last_update)
            mins, secs = divmod(remaining.seconds, 60)
            raise HTTPException(
                status_code=403,
                detail=f"Cuenta bloqueada. Intente de nuevo en {mins} min {secs} seg."
            )
        else:
            # Resetear intentos si ya pasó el tiempo de bloqueo
            db.execute(
                text("UPDATE users SET failed_attempts = 0 WHERE id = :id"),
                {"id": db_user["id"]}
            )
            db.commit()

    # 4️⃣ Verificar contraseña
    if not pwd_context.verify(user.password, db_user["password_hash"]):
        if role != "admin":  # admin no acumula intentos
            new_attempts = db_user["failed_attempts"] + 1
            db.execute(
                text("UPDATE users SET failed_attempts = :fa, updated_at = NOW() WHERE id = :id"),
                {"fa": new_attempts, "id": db_user["id"]}
            )
            db.commit()

            remaining = MAX_ATTEMPTS - new_attempts
            if remaining > 0:
                raise HTTPException(
                    status_code=401,
                    detail=f"Credenciales inválidas. Intentos fallidos: {new_attempts}/{MAX_ATTEMPTS}. "
                           f"Te quedan {remaining} intentos."
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail=f"Cuenta bloqueada por {LOCK_TIME_MINUTES} minutos."
                )
        else:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # 5️⃣ Login exitoso → resetear intentos
    db.execute(
        text("UPDATE users SET failed_attempts = 0 WHERE id = :id"),
        {"id": db_user["id"]}
    )
    db.commit()

    # 6️⃣ Construir objeto UserResponse
    user_response = UserResponse(
        id=db_user["id"],
        name=db_user["name"],
        email=db_user["email"],
        role=role,
        company_id=db_user.get("company_id"),
        department_id=db_user.get("department_id")
    )

    # 7️⃣ Crear token con rol
    token = create_access_token({
        "sub": db_user["email"],
        "role": role
    })

    # 8️⃣ Devolver LoginResponse
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=user_response
    )
