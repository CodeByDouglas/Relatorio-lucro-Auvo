from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.user import User
from app.models.produtos import Produtos
from app.models.tipos_de_tarefas import Tipos_de_tarefas
from app.controller.filtro.carregar_filtros_geral import filtro_bp

@filtro_bp.route('/filtro/carregar_filtros_produtos', methods=['GET'])
def carregar_filtros_produtos():
    if request.method == 'GET':
        api_key = request.args.get('api_key')
        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            # Buscar dados dos produtos do usuário
            tipos_tarefa = Tipos_de_tarefas.query.filter_by(user_id=user_id).first()
           
            # Buscar dados dos produtos do usuário
            produtos = Produtos.query.filter_by(user_id=user_id).first()
            
            lista_produtos_filtrada = []
            if produtos and produtos.json_lista_produtos:
                json_lista_produtos = produtos.json_lista_produtos
                
                for produto in json_lista_produtos:
                    lista_produtos_filtrada.append({
                        'id-produto': produto['id-produto'],
                        'nome-do-produto': produto['nome-do-produto']
                    })
            
            tipos_tarefa_data = []
            if tipos_tarefa and tipos_tarefa.json_lista_tipos_de_tarefas:
                tipos_tarefa_data = tipos_tarefa.json_lista_tipos_de_tarefas
            
            return jsonify({
                'produtos': lista_produtos_filtrada,
                'tipos_tarefa': tipos_tarefa_data
            }), 200
        else:
            return jsonify({"message": "user não autenticado"}), 401 
        


"""
Response do endpoint: 

{
    "produtos": [
        {
            "id-produto": "5a17e0b1-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO CURVA REGULÁVEL P/CANALETA 60MM"
        },
        {
            "id-produto": "5a17e36b-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO CURVA REGULÁVEL P/CANALETA 80MM"
        },
        {
            "id-produto": "5a17e5d5-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO CURVO P/CANALETA 60MM"
        },
        {
            "id-produto": "5a17e810-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO CURVO P/CANALETA 60MM CURVA EXTERNA"
        },
        {
            "id-produto": "5a17ea62-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO CURVO P/CANALETA 80MM"
        },
        {
            "id-produto": "5a17ee08-80b4-11ef-ab1c-0ab8a76e2462",
            "nome-do-produto": "ACABAMENTO DE PASSAGEM P/CANALETA 60MM"
        },
        {
            "id-produto": "f2170118-5eda-11f0-ba85-0a44e9849753",
            "nome-do-produto": "Transdutor"
        },
        {
            "id-produto": "9854b8e3-5fa5-11f0-ba85-0a44e9849753",
            "nome-do-produto": "Produto de teste"
        },
        {
            "id-produto": "c5cdffde-5fa5-11f0-ba85-0a44e9849753",
            "nome-do-produto": "Transdutor 43"
        },
        {
            "id-produto": "1f58d4ed-610d-11f0-ba85-0a44e9849753",
            "nome-do-produto": "Produto para testes"
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