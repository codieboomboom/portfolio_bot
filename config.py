import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "unknown"
    TELEGRAM_BOT_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or "localhost"