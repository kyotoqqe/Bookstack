import os

from pydantic_settings import BaseSettings, SettingsConfigDict


from sqlalchemy import URL

ENV_PATH = path = os.path.join(os.path.dirname(__file__),"..","..",".env")

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)

    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_HOST:str
    POSTGRES_PORT:int

    @property
    def get_db_url(self):
        url = URL.create(
        drivername="postgresql+asyncpg",
        username=self.POSTGRES_USER,
        password=self.POSTGRES_PASSWORD,
        database=self.POSTGRES_DB,
        host=self.POSTGRES_HOST,
        port=self.POSTGRES_PORT
    )

        return url.render_as_string(hide_password=False)