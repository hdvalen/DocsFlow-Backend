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
        subject="🔒 Recuperación de contraseña - DocsFlow",
        recipients=[data.email],
        body=f"""
        <html>
        <body style="margin:0; padding:0; font-family: 'Arial', sans-serif; background-color:#f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding: 20px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); padding: 30px;">
                            <tr>
                                <td align="center" style="padding-bottom: 20px;">
                                    <h2 style="color: #0d6efd; margin:0;">Restablece tu contraseña</h2>
                                </td>
                            </tr>
                            <tr>
                                <td style="color:#333; font-size:16px; line-height:1.5; padding-bottom: 20px;">
                                    Hola,<br><br>
                                    Hemos recibido una solicitud para restablecer tu contraseña en <strong>DocsFlow</strong>.<br>
                                    Haz clic en el botón de abajo para crear una nueva contraseña.
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding-bottom: 30px;">
                                    <a href="{reset_link}" 
                                    style="display:inline-block; padding: 12px 25px; background-color:#0d6efd; color:#ffffff; 
                                            text-decoration:none; border-radius:8px; font-weight:bold; font-size:16px;">
                                        Restablecer contraseña
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td style="font-size:14px; color:#888; text-align:center; border-top:1px solid #ddd; padding-top:20px;">
                                    Si no solicitaste este cambio, ignora este correo.<br>
                                    © 2025 DocsFlow. Todos los derechos reservados.
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return {"msg": "Se ha enviado un email con instrucciones"}


@router.post("/reset-password")
def reset_password(data: ResetPassword, session: Session = Depends(get_db)):
    result = reset_user_password(data.token, data.new_password, data.confirm_password, session)
    return result
