import jwt
from passlib.context import CryptContext

from src.config import settings

from datetime import datetime, timezone, timedelta

JWT_SECRET = settings.jwt_secret
ALGHORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], 
                bcrypt__rounds=12, 
                deprecated="auto")

def generate_password_hash(password:str):
    password_hash = pwd_context.hash(password)
    return password_hash

def verify_passwords(input_password, user_password) -> bool:
    return pwd_context.verify(input_password, user_password)

def generate_jwt_token(user_data):
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_data["exp"] = exp_time
    access_token = jwt.encode(user_data, JWT_SECRET, ALGHORITM)
    return access_token

def decode_jwt_token(token:str):
    try:
        user_data = jwt.decode(token,JWT_SECRET,ALGHORITM)
        return user_data
    except jwt.ExpiredSignatureError:
        return "expired"