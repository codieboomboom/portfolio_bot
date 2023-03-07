from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevConfig
import logging

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    app.logger.setLevel(logging.DEBUG)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprint register
    # Note that we can do away with blueprint too but need to put routes code here, then @app.route can work
    app.register_blueprint(webhook_bp)

    app.logger.debug(f"Running with Config {app.config}")

    return app


from bot_app import models
from bot_app.routes import webhook_bp
