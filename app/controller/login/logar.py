from flask import request, jsonify
from flask import Blueprint
from app.models.user import User
from app.Api.authe_api_auvo import autenticar_api_auvo
from app import db
from datetime import datetime, timedelta
from app.controller.sync.def_sync import sync

login_bp = Blueprint('login_controller', __name__)

@login_bp.route('/logar', methods=['POST'])
def logar():
    if request.method == 'POST':
        api_key = request.json.get('api_key')
        api_token = request.json.get('api_token')
        
        resultado = autenticar_api_auvo(api_key, api_token)
        
        if resultado[0] == 200:
            if resultado[1] == True:
                expiration = resultado[2]
                accessToken = resultado[3]
                
                expiration_datetime = datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S')
                user = User.query.filter_by(api_key=api_key).first()
                if user:
                    user.api_token = api_token
                    user.accessToken = accessToken
                    user.expiracao = expiration_datetime
                    db.session.commit()
                    
                    # Chamada da função sync
                    hoje = datetime.now().date()
                    ontem = hoje - timedelta(days=1)
                    start_date = ontem.strftime('%Y-%m-%d')
                    end_date = hoje.strftime('%Y-%m-%d')
                    
                    resultado_sync = sync(user.id, accessToken, None, None, None, start_date, end_date, None, None)
                    
                    if resultado_sync[0] == False:
                        return jsonify({"message": resultado_sync[1]}), 400
                    else:
                        return jsonify({"message": "Usuario atualizado com sucesso"}), 200
                else:
                    user = User(api_key=api_key, api_token=api_token, accessToken=accessToken, expiracao=expiration_datetime)
                    db.session.add(user)
                    db.session.commit()
                    
                    # Chamada da função sync
                    hoje = datetime.now().date()
                    ontem = hoje - timedelta(days=1)
                    start_date = ontem.strftime('%Y-%m-%d')
                    end_date = hoje.strftime('%Y-%m-%d')
                    
                    resultado_sync = sync(user.id, accessToken, None, None, None, start_date, end_date, status=None, id_colaborador=None)
                    
                    if resultado_sync[0] == False:
                        return jsonify({"message": resultado_sync[1]}), 400
                    else:
                        return jsonify({"message": "Usuario criado com sucesso"}), 200
            else:
                return jsonify({"message": "Credenciais invalidas"}), 401
        elif resultado[0] == 400:
            return jsonify({"message": "api_key e api_token são necessários"}), 400
        elif resultado[0] == 500:
            return jsonify({"message": "não foi possivel se conectar a api AUVO"}), 500
        else:
            return jsonify({"message": "erro interno"}), 500