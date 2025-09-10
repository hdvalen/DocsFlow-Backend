from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database.database import get_db
from app.controllers.users.UsersController import UsersController
from app.auth.dependencies import get_current_user
from app.schemas.Users.UsersSchema import UserRegisterRequest
from app.models.users.UsersModel import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    users_exist = db.exec(select(User)).first()

    if not users_exist:
        return UsersController.register_user(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            db=db,
            role_name="admin"
        )

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo un administrador puede registrar usuarios")

    role_name = user_data.role if user_data.role else "user"

    return UsersController.register_user(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        db=db,
        current_user=current_user,
        role_name=role_name
    )
