from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/microsaas"
    CLERK_SECRET_KEY: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
