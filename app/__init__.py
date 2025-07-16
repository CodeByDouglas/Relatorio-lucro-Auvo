from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuração
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Inicialização das extensões
    db.init_app(app)
    
    # Registro das rotas
    from app.routes import main
    app.register_blueprint(main.main)
    
    # Criação das tabelas se não existirem
    with app.app_context():
        db.create_all()
    
    return app