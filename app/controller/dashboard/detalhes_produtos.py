from flask import request, jsonify
from app.controller.dashboard.dashboard_geral import dashboard_controller_bp
from app.controller.login.check_auth import check_auth
from app.models.user import User
from app.models.tarefas import Tarefas

@dashboard_controller_bp.route('/detalhes_produtos', methods=['GET'])
def detalhes_produtos():
    if request.method == 'GET':
        api_key = request.args.get('api_key')
        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id

            tarefas = Tarefas.query.filter_by(user_id=user_id).first()
            
            if tarefas and tarefas.json_lista_tarefas:
                lista_tarefas = tarefas.json_lista_tarefas
                resultado = []
                for tarefa in lista_tarefas:
                    novo_obj = {
                        "id-da-tarefa": tarefa.get("id-da-tarefa"),
                        "data-da-tarefa": tarefa.get("data-da-tarefa", "")[:10],
                        "nome-do-cliente": tarefa.get("nome-do-cliente"),
                        "faturamento-total": tarefa.get("faturamento-produtos"),
                        "lucro-total": tarefa.get("lucro-produto")
                    }
                    resultado.append(novo_obj)
                return jsonify(resultado), 200
            else:
                return jsonify([]), 200
            
            
        
        else:
            return jsonify({"message": "user não autenticado"}), 401
        



"""
Response do endpoint: 
[
    {
        "data-da-tarefa": "2025-07-21",
        "faturamento-total": 750.0,
        "id-da-tarefa": 61086690,
        "lucro-total": 500.0,
        "nome-do-cliente": "Condomínio Auvo"
    },
    {
        "data-da-tarefa": "2025-07-21",
        "faturamento-total": 500.0,
        "id-da-tarefa": 61125002,
        "lucro-total": 250.0,
        "nome-do-cliente": "Cliente de Teste"
    },
    {
        "data-da-tarefa": "2025-07-21",
        "faturamento-total": 500.0,
        "id-da-tarefa": 61125028,
        "lucro-total": 250.0,
        "nome-do-cliente": "Cliente de Teste"
    },
    {
        "data-da-tarefa": "2025-07-21",
        "faturamento-total": 500.0,
        "id-da-tarefa": 61125029,
        "lucro-total": 250.0,
        "nome-do-cliente": "Cliente de Teste"
    },
    {
        "data-da-tarefa": "2025-07-21",
        "faturamento-total": 500.0,
        "id-da-tarefa": 61125030,
        "lucro-total": 250.0,
        "nome-do-cliente": "Cliente de Teste"
    },

"""
