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
import config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_views, question_views, answer_views, food_views, image_processing_views
    from . import models

    # blueprint
    app.register_blueprint(main_views.bp)
    # app.register_blueprint(question_views.bp)
    # app.register_blueprint(answer_views.bp)
    app.register_blueprint(food_views.bp)
    app.register_blueprint(image_processing_views.bp)
    return app
