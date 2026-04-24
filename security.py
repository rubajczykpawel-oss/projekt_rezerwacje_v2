from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "tajny_klucz_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Token jest niepoprawny lub wygasł")