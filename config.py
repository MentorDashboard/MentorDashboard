import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = os.getenv('FLASK_ENV') or 'production'
    SECRET_KEY = os.getenv('SECRET_KEY')
