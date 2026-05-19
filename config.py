import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv
    if os.getenv("APP_ENV", "local").lower() == "local":
        load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-secret-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    BASE_DIR = str(BASE_DIR)
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")


class LocalConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'local.db'}"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    if SQLALCHEMY_DATABASE_URI is None:
        raise RuntimeError("DATABASE_URL is required in production.")


def get_config():
    env = os.getenv("APP_ENV", "local").lower()#This allows us to specify the environment (local, production, etc.) using an environment variable. If not set, it defaults to "local".  
    if env in ("production", "prod", "deploy"):
        return ProductionConfig
    return LocalConfig
