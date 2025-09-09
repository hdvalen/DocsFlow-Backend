from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.security import hash_password
from app.auth.AuthJwtHandler import create_access_token

class UsersController:

    @staticmethod
    def register_user(name: str, email: str, password: str, db: Session, current_user=None, role_name: str = None):
        """
        Registra un nuevo usuario.
        - Si no hay admin creado, el primer usuario será 'admin'.
        - Si hay admin, solo un admin puede crear usuarios y puede asignar 'user' o 'admin'.
        """

        # Revisar si ya existe algún admin
        admin_exists = db.execute(text("""
            SELECT 1
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id
            JOIN roles r ON ur.role_id = r.id
            WHERE r.name = 'admin'
            LIMIT 1
        """)).first()

        if admin_exists:
            # Solo admin puede crear nuevos usuarios
            if not current_user or current_user.get("role") != "admin":
                raise HTTPException(status_code=403, detail="No autorizado para registrar usuarios")
        else:
            # No hay admin, el primer usuario será admin
            role_name = "admin"

        # Si no se pasó un rol y ya existe admin, asignar por defecto 'user'
        if not role_name:
            role_name = "user"

        # Verificar si el rol existe en la tabla roles
        role_row = db.execute(text("SELECT id FROM roles WHERE name = :name"), {"name": role_name}).first()
        if not role_row:
            raise HTTPException(status_code=400, detail=f"El rol '{role_name}' no existe en la base de datos")
        role_id = role_row[0]

        # Verificar si el email ya está registrado
        existing = db.execute(text("SELECT 1 FROM users WHERE email = :email"), {"email": email}).first()
        if existing:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Hashear la contraseña
        hashed = hash_password(password)

        # Insertar el usuario
        query = text("""
            INSERT INTO users (name, email, password_hash, is_active, failed_attempts)
            VALUES (:name, :email, :password_hash, 1, 0)
        """)
        result = db.execute(query, {"name": name, "email": email, "password_hash": hashed})
        db.commit()

        # Obtener el id del nuevo usuario
        new_user_id = result.lastrowid

        # Asignar rol
        db.execute(
            text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
            {"user_id": new_user_id, "role_id": role_id}
        )
        db.commit()

        # Generar token para el nuevo usuario
        token = create_access_token({"sub": email, "role": role_name})

        return {"message": f"Usuario registrado exitosamente con rol {role_name}", "access_token": token}
