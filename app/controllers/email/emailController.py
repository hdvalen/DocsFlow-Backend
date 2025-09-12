import secrets
from datetime import datetime, timedelta
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from app.database.database import get_db

from app.models.email.emailModel import PasswordResetToken
from app.models.users.UsersModel import User 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_password_reset_token(email: str, db: Session = Depends(get_db)) -> str:

    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    token = secrets.token_urlsafe(32)

    old_token = db.exec(
        select(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
    ).first()
    if old_token:
        db.delete(old_token)
        db.commit()

    reset_token = PasswordResetToken(user_id=user.id, token=token)
    db.add(reset_token)
    db.commit()

    return token

from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.users.UsersModel import User
from app.models.email.emailModel import PasswordResetToken
from app.core.security import pwd_context

def reset_user_password(token: str, new_password: str, confirm_password: str, db: Session) -> bool:
    # Buscar token
    token_obj = db.exec(select(PasswordResetToken).where(PasswordResetToken.token == token)).first()
    if not token_obj:
        return False  # Token inválido

    # Revisar expiración (1 hora)
    if datetime.utcnow() > token_obj.created_at + timedelta(hours=1):
        db.delete(token_obj)
        db.commit()
        return False  # Token expirado

    # Buscar usuario
    user = db.get(User, token_obj.user_id)
    if not user:
        return False

    # Verificar contraseñas
    if new_password != confirm_password:
        return False

    # Actualizar contraseña
    user.password_hash = pwd_context.hash(new_password)
    db.add(user)

    # Eliminar token
    db.delete(token_obj)
    db.commit()

    return True
