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
    from app.routes.login import login_bp
    from app.routes.dashboard_geral import dashboard_bp
    from app.controller.login.logar import login_bp as controller_login_bp
    from app.controller.sync.sync_controler import sync_bp
    from app.controller.dashboard.dashboard_geral import dashboard_controller_bp
    from app.controller.dashboard import dashboard_produtos  # Importa para registrar as rotas
    from app.controller.dashboard import dashboard_serviços  # Importa para registrar as rotas
    from app.controller.filtro.carregar_filtros_geral import filtro_bp
    from app.controller.filtro import carregar_filtros_produtos  # Importa para registrar as rotas
    from app.controller.filtro import carregar_filtros_servicos  # Importa para registrar as rotas
    
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(controller_login_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(dashboard_controller_bp)
    app.register_blueprint(filtro_bp)
    
    # Criação das tabelas se não existirem
    with app.app_context():
        db.create_all()
    
    return app