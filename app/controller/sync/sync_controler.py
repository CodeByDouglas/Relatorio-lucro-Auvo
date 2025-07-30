from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.controller.sync.def_sync import sync

sync_bp = Blueprint('sync_controller', __name__)

@sync_bp.route('/sync', methods=['POST'])
def sync_endpoint():
    if request.method == 'POST':
        api_key = request.json.get('api_key')
        id_produto = request.json.get('id_produto')
        id_servico = request.json.get('id_servico')
        id_tipo_de_tarefa = request.json.get('id_tipo_de_tarefa')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        status = request.json.get('status')
        resultado = check_auth(api_key)
        
        if resultado[0] == False:
            return jsonify({"message": resultado[1]}), 401
        else:
            # Buscar user_id através da api_key
            from app.models.user import User
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            sincronizacao = sync(user_id, resultado[2], id_produto, id_servico, id_tipo_de_tarefa, start_date, end_date, status)
            
            if sincronizacao[0] == True:
                return jsonify({"message": "Sincronização realizada com sucesso"}), 200
            else: 
                return jsonify({"message": sincronizacao[1]}), 400

                
