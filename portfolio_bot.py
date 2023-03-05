from app import create_app
from config import ProductionConfig

if __name__ == "__main__":
    app_instance = create_app(ProductionConfig)
    app_instance.run(debug=True)
