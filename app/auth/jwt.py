
from datetime import datetime, timedelta, UTC
from app.core.settings import env
from jose import JWTError, jwt

def create_access_token(
    data: dict,
    expires_delta: int = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
):
    to_encode = data.copy()

    expire = datetime.now(UTC) + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, env.ACCESS_TOKEN_SECRET_KEY, algorithm=env.ACCESS_TOKEN_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, env.ACCESS_TOKEN_SECRET_KEY, algorithms=[env.ACCESS_TOKEN_ALGORITHM])
        return payload
    except JWTError as e:
        print(e)
        print("Error decoding token")
        return

