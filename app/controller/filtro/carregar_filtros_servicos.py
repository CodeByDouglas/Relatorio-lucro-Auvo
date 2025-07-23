from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.user import User
from app.models.servicos import Servicos
from app.models.tipos_de_tarefas import Tipos_de_tarefas
from app.controller.filtro.carregar_filtros_geral import filtro_bp

@filtro_bp.route('/filtro/carregar_filtros_servicos', methods=['GET'])
def carregar_filtros_servicos():
    if request.method == 'GET':
        api_key = request.args.get('api_key')
        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            # Buscar dados dos produtos do usuário
            tipos_tarefa = Tipos_de_tarefas.query.filter_by(user_id=user_id).first()
           
            # Buscar dados dos produtos do usuário
            servicos = Servicos.query.filter_by(user_id=user_id).first()
            
            servicos_data = []
            if servicos and servicos.json_lista_servicos:
                servicos_data = servicos.json_lista_servicos
                
            
            tipos_tarefa_data = []
            if tipos_tarefa and tipos_tarefa.json_lista_tipos_de_tarefas:
                tipos_tarefa_data = tipos_tarefa.json_lista_tipos_de_tarefas
            
            return jsonify({
                'servicos': servicos_data,
                'tipos_tarefa': tipos_tarefa_data
            }), 200
        else:
            return jsonify({"message": "user não autenticado"}), 401 
        

"""
Response do endpoint:

{
    "servicos": [
        {
            "id-servico": "5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Higienização"
        },
        {
            "id-servico": "5a1b313b-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Limpeza de Condensador"
        },
        {
            "id-servico": "5a1b31fe-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Mão de Obra"
        },
        {
            "id-servico": "5a1b327d-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Regarga de Gás"
        },
        {
            "id-servico": "5a1b32ed-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Reparo no Termostato"
        },
        {
            "id-servico": "5a1b3360-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Troca de Motoventilador"
        },
        {
            "id-servico": "5a1b33cf-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-servico": "Troca de Termostato"
        },
        {
            "id-servico": "b28117c7-626b-4b53-8462-ff04b4af1a14",
            "nome-do-servico": "Mão de obra"
        }
    ],
    "tipos_tarefa": [
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
}
"""