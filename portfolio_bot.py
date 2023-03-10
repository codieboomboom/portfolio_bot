import os
from bot_app import create_app
from config import DevConfig, ProductionConfig


if __name__ == "__main__":
    is_production = True if "PRODUCTION_SERVER" in os.environ else False
    if is_production:
        app_instance = create_app(ProductionConfig)
    else:
        app_instance = create_app(DevConfig)
    app_instance.run()
