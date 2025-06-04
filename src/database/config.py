import os

from pydantic_settings import BaseSettings, SettingsConfigDict


from sqlalchemy import URL

ENV_PATH = path = os.path.join(os.path.dirname(__file__),"..","..",".env")

class DatabaseSettings(BaseSettings):
    postgres_user:str
    postgres_password:str
    postgres_db:str
    postgres_host:str
    postgres_port:int

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")

    @property
    def get_db_url(self):
        url = URL.create(
        drivername="postgresql+asyncpg",
        username=self.postgres_user,
        password=self.postgres_password,
        database=self.postgres_db,
        host=self.postgres_host,
        port=self.postgres_port
    )

        return url.render_as_string(hide_password=False)