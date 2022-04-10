import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = os.getenv("FLASK_ENV") or "production"
    SECRET_KEY = os.getenv("SECRET_KEY")
    if os.getenv("FLASK_ENV") == "development":
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
