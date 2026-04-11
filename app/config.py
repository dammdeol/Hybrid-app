import os


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Hybrid Flask + FastAPI")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")


settings = Settings()