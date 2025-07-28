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
    from app.routes.dashboard_produtos import dashboard_produtos_bp
    from app.routes.dashboard_servicos import dashboard_servicos_bp
    from app.controller.login.logar import login_bp as controller_login_bp
    from app.controller.sync.sync_controler import sync_bp
    from app.controller.dashboard.dashboard_geral import dashboard_controller_bp
    from app.controller.dashboard import dashboard_produtos  
    from app.controller.dashboard import dashboard_serviços 
    from app.controller.dashboard import detalhes_geral  
    from app.controller.dashboard import detalhes_produtos  
    from app.controller.dashboard import detalhes_servicos  
    from app.controller.filtro.carregar_filtros_geral import filtro_bp
    from app.controller.filtro import carregar_filtros_produtos  
    from app.controller.filtro import carregar_filtros_servicos  
    from app.controller.Planilha.planilha_geral import planilha_bp
    from app.controller.Planilha.planilha_produtos import planilha_produtos_bp
    from app.controller.Planilha.planilha_servicos import planilha_servicos_bp
    
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(dashboard_produtos_bp)
    app.register_blueprint(dashboard_servicos_bp)
    app.register_blueprint(controller_login_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(dashboard_controller_bp)
    app.register_blueprint(filtro_bp)
    app.register_blueprint(planilha_bp)
    app.register_blueprint(planilha_produtos_bp)
    app.register_blueprint(planilha_servicos_bp)
    
    # Redirecionar a URL raiz para /login
    @app.route('/')
    def index():
        from flask import redirect
        return redirect('/login')
    
    # Criação das tabelas se não existirem
    with app.app_context():
        db.create_all()
    
    return app