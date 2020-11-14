import sentry_sdk
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
bcrypt = Bcrypt()


def create_app(config_class=Config):
    templates_path = path.abspath(path.join(path.dirname(__file__), "templates"))
    static_path = path.abspath(
        path.join(path.dirname(__file__), "..", "assets", "build")
    )

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    app.config.from_object(config_class)

    sentry_sdk.init(
        dsn=app.config["SENTRY_DSN"],
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
        ],
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)

    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.students import bp as students_bp
    from app.routes.users import bp as users_bp
    from app.routes.reports import bp as reports_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(reports_bp)

    return app
