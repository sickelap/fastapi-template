from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def find_dotenv(start: Path = Path.cwd(), filename: str = ".env") -> Path | None:
    for parent in [start] + list(start.parents):
        env_path = parent / filename
        if env_path.is_file():
            return env_path


class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SQLALCHEMY_DATABASE_URL: str = ""
    ALLOW_REGISTER: bool = True

    model_config = SettingsConfigDict(env_file=find_dotenv(), env_file_encoding="utf-8")


settings = Settings()
