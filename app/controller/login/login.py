from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.user import User
from app.Api.authe_api_auvo import autenticar_api_auvo

login_controller = Blueprint('login_controller', __name__)

@login_controller.route('/login', methods=['POST'])
def login_endpoint():
    """
    Endpoint para login/cadastro de usuário
    
    Recebe POST com parâmetros:
    - api_key: Chave da API
    - token: Token da API
    
    Returns:
        JSON: Resultado do login/cadastro ou erro
    """
    try:
        # Obter dados do request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        api_key = data.get('api_key')
        token = data.get('token')
        
        if not api_key or not token:
            return jsonify({"error": "api_key e token são obrigatórios"}), 400
        
        # Autenticar na API da Auvo
        access_token = autenticar_api_auvo(api_key, token)
        
        if not access_token:
            return jsonify({"error": "Falha na autenticação"}), 401
        
        # Cadastrar usuário no banco
        novo_user = User(
            api_key=api_key,
            token=token,
            token_autenticacao=access_token,
            horario_da_ultima_autenticacao=datetime.now()
        )
        
        db.session.add(novo_user)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário cadastrado com sucesso",
            "user_id": novo_user.id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
