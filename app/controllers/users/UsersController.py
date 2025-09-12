from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlmodel import select
from app.core.security import hash_password, create_access_token
from app.models.users.UsersModel import User
from app.schemas.Users.UsersSchema import UserResponse
from app.schemas.Documents.DocumentsSchema import DocumentResponse
class UsersController:

    @staticmethod
    def er_user(name: str, email: str, password: str, db: Session, role_name: str = None):
        # Verificar si ya existe algún admin
        admin_exists = db.execute(text("""
            SELECT 1
            FROM users u
            JOIN user_roles ur ON u.id = ur.user_id
            JOIN roles r ON ur.role_id = r.id
            WHERE r.name = 'admin'
            LIMIT 1
        """)).first()

        if not admin_exists:
            role_name = "admin"
        else:
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

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        user = db.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsersController.format_user_response(user, db)

    @staticmethod
    def format_user_response(user: User, db: Session):
        # Obtener rol
        role_row = db.execute(
            text("""
                SELECT r.name
                FROM roles r
                JOIN user_roles ur ON ur.role_id = r.id
                WHERE ur.user_id = :id
            """), {"id": user.id}
        ).first()
        role = role_row[0] if role_row else "user"

        # Obtener documentos del usuario
        docs_rows = db.execute(
            text("""
                SELECT id, department_id, doc_type_id, company_id, title, original_filename, uploaded_at, processed
                FROM documents
                WHERE uploaded_by = :user_id
            """), {"user_id": user.id}
        ).mappings().all()

        documents = [
            DocumentResponse(
                id=d["id"],
                department_id=d["department_id"],
                doc_type_id=d["doc_type_id"],
                company_id=d["company_id"],
                title=d["title"],
                original_filename=d["original_filename"],
                uploaded_at=d["uploaded_at"],
                processed=d["processed"]
            ) for d in docs_rows
        ]

        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=role,
            company_id=user.company_id,
            department_id=user.department_id,
            documents=documents  # <--- añadimos la lista de documentos
        )

