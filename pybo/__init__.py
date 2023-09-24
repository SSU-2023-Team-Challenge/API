# def create_app():
#     app = Flask(__name__)
#     # blueprint
#     from.views import main_views
#     app.register_blueprint(main_views.bp)
#
#     return app

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # app.config.from_envvar('APP_CONFIG_FILE')
    app.config.from_object('config.development')

    CORS(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_views, menu_views, image_processing_views
    from . import models

    # blueprint
    app.register_blueprint(main_views.bp)
    app.register_blueprint(menu_views.bp)
    app.register_blueprint(image_processing_views.bp)
    return app
