import os
from flask import Flask

from config import Config


def create_app(config_class=Config):
    templates_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))

    app = Flask(__name__, template_folder=templates_path)
    app.config.from_object(config_class)

    from src.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
