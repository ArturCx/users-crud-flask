from flask import Flask
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]

def create_app():
    app = Flask(__name__)
    
    # Registra as rotas
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app