from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.dados_calculados import Faturamento_total, Lucro_total, Faturamento_produtos, Faturamento_servicos, Lucro_produtos, Lucro_servicos
from app.models.user import User

dashboard_controller_bp = Blueprint('dashboard_controller', __name__, url_prefix='/dados')

@dashboard_controller_bp.route('/dashboard_geral', methods=['GET'])
def dados_dashboard_geral():
        api_key = request.args.get('api_key')

        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            faturamento_total = Faturamento_total.query.filter_by(user_id=user_id).first()
            lucro_total = Lucro_total.query.filter_by(user_id=user_id).first()
            faturamento_produtos = Faturamento_produtos.query.filter_by(user_id=user_id).first()
            faturamento_servicos = Faturamento_servicos.query.filter_by(user_id=user_id).first()
            lucro_produtos = Lucro_produtos.query.filter_by(user_id=user_id).first()
            lucro_servicos = Lucro_servicos.query.filter_by(user_id=user_id).first()
            
            return jsonify({
                "faturamento_total": {
                    "valor": faturamento_total.valor,
                    "porcentagem_total_faturamento": faturamento_total.porcentagem_total_faturamento
                },
                "lucro_total": {
                    "valor": lucro_total.valor,
                    "porcentagem_faturamento_total": lucro_total.porcentagem_faturamento_total
                },
                "faturamento_produtos": {
                    "valor": faturamento_produtos.valor,
                    "porcentagem_faturamento_total": faturamento_produtos.porcentagem_faturamento_total
                },
                "faturamento_servicos": {
                    "valor": faturamento_servicos.valor,
                    "porcentagem_faturamento_total": faturamento_servicos.porcentagem_faturamento_total
                },
                "lucro_produtos": {
                    "valor": lucro_produtos.valor,
                    "porcentagem_lucro_total": lucro_produtos.porcentagem_lucro_total
                },
                "lucro_servicos": {
                    "valor": lucro_servicos.valor,
                    "porcentagem_lucro_total": lucro_servicos.porcentagem_lucro_total
                }
            }), 200
        
        else:
            return jsonify({"message": "user não autenticado"}), 401 
