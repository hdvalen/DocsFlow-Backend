from fastapi import HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session
from app.database.database import get_db
from app.core.security import hash_password, verify_password, create_access_token

class UsersController:

    @staticmethod
    def register_user(name: str, email: str, password: str, db: Session):
        # Verificar si existe
        existing = db.exec(text("SELECT * FROM users WHERE email = :email"), {"email": email}).first()
        if existing:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        hashed = hash_password(password)
        query = text("""
            INSERT INTO users (name, email, password_hash, is_active, failed_attempts)
            VALUES (:name, :email, :password_hash, 1, 0)
        """)
        db.exec(query, {"name": name, "email": email, "password_hash": hashed})
        db.commit()
        return {"message": "Usuario registrado exitosamente"}

    @staticmethod
    def login_user(email: str, password: str, db: Session):
        user = db.exec(text("SELECT * FROM users WHERE email = :email"), {"email": email}).first()
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not verify_password(password, user.password_hash):
            db.exec(text("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE id = :id"), {"id": user.id})
            db.commit()
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = create_access_token({"sub": str(user.id), "email": user.email})
        return {"access_token": token, "token_type": "bearer"}
