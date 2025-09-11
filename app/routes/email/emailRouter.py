# controllers/auth.py

from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.email.emailController import create_password_reset_token, reset_user_password
from app.controllers.email.emailConfiguracion import conf
from app.models.email.emailModel import PasswordResetRequest, ResetPassword
from fastapi_mail import FastMail, MessageSchema

router = APIRouter()


@router.post("/password-reset-request")
async def password_reset_request(data: PasswordResetRequest, db: Session = Depends(get_db)):
    token = create_password_reset_token(data.email, db)

    reset_link = f"http://localhost:8000/reset-password-form?token={token}"
    message = MessageSchema(
        subject="Recuperación de contraseña",
        recipients=[data.email],
        body=f"Da click en el siguiente enlace para restablecer tu contraseña:\n\n{reset_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return {"msg": "Se ha enviado un email con instrucciones"}


@router.post("/reset-password")
def reset_password(data: ResetPassword, session: Session = Depends(get_db)):
    result = reset_user_password(data.token, data.new_password, session)
    return result
