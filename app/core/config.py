from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    database_url: str = 'sqlite+aiosqlite:///./cats.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'superuser@email.com'
    first_superuser_password: Optional[str] = 'password'

    class Config:
        env_file = '.env'


settings = Settings()
