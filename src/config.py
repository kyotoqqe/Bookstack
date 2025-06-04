import os

from pydantic import EmailStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = path = os.path.join(os.path.dirname(__file__), "..",".env")



class Settings(BaseSettings):
    base_url:HttpUrl
    jwt_secret:str

    postgres_user:str
    postgres_password:str
    postgres_db:str
    postgres_host:str
    postgres_port:int

    email_sender:EmailStr
    email_passcode:str
    smtp_host:str
    smtp_port:int

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")
    
settings = Settings()