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


def reset_user_password(token: str, new_password: str, session: Session):

    statement = select(PasswordResetToken).where(PasswordResetToken.token == token)
    token_obj = session.exec(statement).first()
    if not token_obj:
        raise HTTPException(status_code=400, detail="Token inválido")

    if datetime.utcnow() > token_obj.created_at + timedelta(hours=1):
        session.delete(token_obj)
        session.commit()
        raise HTTPException(status_code=400, detail="Token expirado")

    user = session.get(User, token_obj.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    hashed_password = pwd_context.hash(new_password)
    user.hashed_password = hashed_password
    session.add(user)

    session.delete(token_obj)

    session.commit()

    return {"msg": "Contraseña actualizada con éxito"}
