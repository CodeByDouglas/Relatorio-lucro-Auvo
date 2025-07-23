from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.user import User
from app.models.tipos_de_tarefas import Tipos_de_tarefas

filtro_bp = Blueprint('filtro_controller', __name__)

@filtro_bp.route('/filtro/carregar_filtros_geral', methods=['GET'])
def carregar_filtros_geral():
    if request.method == 'GET':
        api_key = request.args.get('api_key')
        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            # Buscar dados dos tipos de tarefa do usuário
            tipos_tarefa = Tipos_de_tarefas.query.filter_by(user_id=user_id).first()
            
            if tipos_tarefa and tipos_tarefa.json_lista_tipos_de_tarefas:
                return jsonify(tipos_tarefa.json_lista_tipos_de_tarefas), 200
            else:
                return jsonify([]), 200  # Retorna lista vazia se não houver dados
        else:
            return jsonify({"message": "user não autenticado"}), 401
        
"""
Response do endpoint:
[
    {
        "id-tipo-de-tarefa": 182191,
        "nome-do-tipo-de-tarefa": "Chamado"
    },
    {
        "id-tipo-de-tarefa": 192651,
        "nome-do-tipo-de-tarefa": "Fechamento"
    },
    {
        "id-tipo-de-tarefa": 182794,
        "nome-do-tipo-de-tarefa": "Instalação"
    },
    {
        "id-tipo-de-tarefa": 168397,
        "nome-do-tipo-de-tarefa": "Instalação Nova ( com obrigatoriedade )"
    },
    {
        "id-tipo-de-tarefa": 176011,
        "nome-do-tipo-de-tarefa": "Instalação Nova ( Sem obrigatoriedade )"
    },
    {
        "id-tipo-de-tarefa": 168394,
        "nome-do-tipo-de-tarefa": "Manutenção Corretiva"
    },
    {
        "id-tipo-de-tarefa": 174678,
        "nome-do-tipo-de-tarefa": "MANUTENÇÃO CORRETIVA e preventiva"
    },
    {
        "id-tipo-de-tarefa": 168395,
        "nome-do-tipo-de-tarefa": "Manutenção Preventiva"
    },
    {
        "id-tipo-de-tarefa": 196548,
        "nome-do-tipo-de-tarefa": "ManutençãoG"
    },
    {
        "id-tipo-de-tarefa": 168398,
        "nome-do-tipo-de-tarefa": "PMOC"
    },
    {
        "id-tipo-de-tarefa": 188375,
        "nome-do-tipo-de-tarefa": "Sem questionário"
    },
    {
        "id-tipo-de-tarefa": 171987,
        "nome-do-tipo-de-tarefa": "Teste campo largo"
    },
    {
        "id-tipo-de-tarefa": 197535,
        "nome-do-tipo-de-tarefa": "visita clientes prospecção G"
    },
    {
        "id-tipo-de-tarefa": 168396,
        "nome-do-tipo-de-tarefa": "Visita para OrçamentoG"
    }
]
"""

