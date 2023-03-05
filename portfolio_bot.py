from app import create_app
from config import DevConfig

if __name__ == "__main__":
    app_instance = create_app(DevConfig)
    app_instance.run()
