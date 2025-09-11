from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import hash_password, create_access_token

class UsersController:
    @staticmethod
    def register_user(name: str, email: str, password: str, db: Session, role_name: str = None):
        # Verificar si ya existe algún admin
        admin_exists = db.execute(text("""
            SELECT 1
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id
            JOIN roles r ON ur.role_id = r.id
            WHERE r.name = 'admin'
            LIMIT 1
        """)).first()

        # Si no hay admin, el primer usuario registrado será admin
        if not admin_exists:
            role_name = "admin"
        else:
            # Si no se especifica, asignar por defecto 'user'
            if not role_name:
                role_name = "user"

        # Verificar que el rol existe
        role_row = db.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role_name}).first()
        if not role_row:
            raise HTTPException(status_code=400, detail=f"El rol '{role_name}' no existe")
        role_id = role_row[0]

        # Verificar que el email no esté registrado
        existing = db.execute(text("SELECT 1 FROM users WHERE email = :email"), {"email": email}).first()
        if existing:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Hashear contraseña
        hashed = hash_password(password)

        # Crear usuario
        result = db.execute(
            text("""
                INSERT INTO users (name, email, password_hash, is_active, failed_attempts)
                VALUES (:name, :email, :password_hash, 1, 0)
            """),
            {"name": name, "email": email, "password_hash": hashed}
        )
        db.commit()
        new_user_id = result.lastrowid

        # Asignar rol
        db.execute(
            text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
            {"user_id": new_user_id, "role_id": role_id}
        )
        db.commit()

        # Crear token JWT
        token = create_access_token({"sub": email, "role": role_name})
        return {"message": f"Usuario registrado con rol {role_name}", "access_token": token}
