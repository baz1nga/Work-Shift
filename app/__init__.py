import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240,
            backupCount=10,
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]',
        ),
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('WorkShift logging')

    return app
