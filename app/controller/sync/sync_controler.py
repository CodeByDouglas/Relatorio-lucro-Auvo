from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth

sync_bp = Blueprint('sync_controller', __name__)

@sync_bp.route('/sync', methods=['POST'])
def sync():
    if request.method == 'POST':
        api_key = request.json.get('api_key')
        id_produto = request.json.get('id_produto')
        id_servico = request.json.get('id_servico')
        id_tipo_de_tarefa = request.json.get('id_tipo_de_tarefa')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        
        resultado = check_auth(api_key)
        
        if resultado[0] == False:
            return jsonify({"message": resultado[1]}), 401
        else:
            return jsonify({"message": "Autenticado"}), 200
