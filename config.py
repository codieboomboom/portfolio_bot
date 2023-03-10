import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "unknown"
    TELEGRAM_BOT_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or "localhost"

    def __repr__(self):
        return f"Config for production"


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __repr__(self):
        return f"Config for testing"


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "production.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_BOT_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
