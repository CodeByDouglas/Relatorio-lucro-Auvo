from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app import db
from app.models.user import User
from app.Api.authe_api_auvo import autenticar_api_auvo
from app.controller.sync.def_sync import sync

sync_controller = Blueprint('sync_controller', __name__)

@sync_controller.route('/sync', methods=['POST'])
def sync_endpoint():
    """
    Endpoint para sincronização de dados
    
    Recebe POST com parâmetros:
    - iduser: ID do usuário
    - filtros: Objeto com filtros de data e IDs
    
    Returns:
        JSON: Resultado da sincronização ou erro
    """
    try:
        # Obter dados do request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        iduser = data.get('iduser')
        filtros = data.get('filtros', {})
        
        if not iduser:
            return jsonify({"error": "iduser é obrigatório"}), 400
        
        # Buscar usuário no banco de dados
        user = User.query.filter_by(id=iduser).first()
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Verificar se precisa renovar token (mais de 28 minutos)
        agora = datetime.now()
        tempo_limite = timedelta(minutes=28)
        
        if (user.horario_da_ultima_autenticacao is None or 
            agora - user.horario_da_ultima_autenticacao > tempo_limite):
            
            # Renovar token
            access_token = autenticar_api_auvo(user.api_key, user.token)
            
            if not access_token:
                return jsonify({"error": "Falha na autenticação"}), 401
            
            # Atualizar token e horário no banco
            user.token_autenticacao = access_token
            user.horario_da_ultima_autenticacao = agora
            db.session.commit()
        
        # Extrair parâmetros dos filtros (None se não fornecidos)
        data_inicial = filtros.get('data_inicial')
        data_final = filtros.get('data_final')
        id_tipo_de_tarefa = filtros.get('id_tipo_de_tarefa')
        ids_produto_filtrado = filtros.get('ids_produto_filtrado')
        ids_servico_filtrado = filtros.get('ids_servico_filtrado')
        
        # Chamar função sync
        resultado = sync(
            data_inicial=data_inicial,
            data_final=data_final,
            id_tipo_de_tarefa=id_tipo_de_tarefa,
            ids_produto_filtrado=ids_produto_filtrado,
            ids_servico_filtrado=ids_servico_filtrado,
            iduser=iduser,
            token_auth=user.token_autenticacao
        )
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
