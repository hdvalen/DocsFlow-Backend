from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Credenciales no encontradas")
        return credentials.credentials


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_user(token: str = Depends(JWTBearer())):
    """
    Extrae y normaliza los datos del usuario desde el JWT.
    """
    payload = decode_access_token(token)

    user_data = {
        "id": payload.get("sub"),  # 👈 ahora siempre tendrás "id"
        "name": payload.get("name"),
        "email": payload.get("email"),
        "role": payload.get("role"),
        "company_id": payload.get("company_id"),
        "department_id": payload.get("department_id"),
    }

    if user_data["id"] is None:
        raise HTTPException(status_code=401, detail="Token inválido: falta id")

    return user_data


def role_required(allowed_roles: list):
    """
    Decorador para validar que el usuario tenga uno de los roles permitidos.
    """
    def wrapper(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return current_user
    return wrapper
