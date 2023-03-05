from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    app.logger.setLevel(logging.INFO)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    app.logger.debug(f"Running with Config {app.config}")

    return app


from app.models import Stock, Crypto, MutualFund
