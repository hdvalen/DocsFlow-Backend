from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from app.auth.AuthJwtHandler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # ruta para login

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return payload

def get_current_user_optional(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return None
        payload = decode_access_token(token)
        return payload
    except Exception:
        return None
