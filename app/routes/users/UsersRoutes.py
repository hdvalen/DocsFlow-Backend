from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.database import get_db
from app.controllers.users.UsersController import UsersController
from app.schemas.Users.UsersSchema import UserRegisterRequest, UserResponse
from app.auth.dependencies import get_current_user, role_required
from app.models.users.UsersModel import User
from typing import List

router = APIRouter()


@router.post("/register")
def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    # No se requiere current_user
    return UsersController.register_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        db=db,
        role_name=user_data.role  # opcional, si quieres permitir que manden el rol (normalmente ignorado)
    )


# 🔹 Endpoint: Obtener info del usuario actual
@router.get("/me", response_model=UserResponse)
def get_my_user(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    email = current_user.get("email") or current_user.get("sub")  # revisa si tu token tiene 'sub'
    return UsersController.get_user_by_email(email, db)


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: dict = Depends(role_required(["admin"]))):
    users = db.exec(select(User)).all()
    return [UsersController.format_user_response(u, db) for u in users]
