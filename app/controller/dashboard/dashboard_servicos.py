from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.dados_calculados import  Faturamento_servicos, Lucro_servicos, Custo_servicos
from app.models.user import User
from app.controller.dashboard.dashboard_geral import dashboard_controller_bp

@dashboard_controller_bp.route('/dashboard_servicos', methods=['GET'])
def dados_dashboard_servicos():
        api_key = request.args.get('api_key')

        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            faturamento_servicos = Faturamento_servicos.query.filter_by(user_id=user_id).first()
            lucro_servicos = Lucro_servicos.query.filter_by(user_id=user_id).first()
            custo_servicos = Custo_servicos.query.filter_by(user_id=user_id).first()
            
            # Calcular a porcentagem do lucro em relação ao faturamento
            porcentagem_lucro = 0
            if faturamento_servicos.valor > 0:
                porcentagem_lucro = (lucro_servicos.valor / faturamento_servicos.valor) * 100
            
            return jsonify({
                "faturamento_servicos": {
                    "valor": faturamento_servicos.valor,
                    "porcentagem_faturamento_total": 100
                },
                "lucro_servicos": {
                    "valor": lucro_servicos.valor,
                    "porcentagem_lucro_total": porcentagem_lucro
                },
                "custo_servicos": {
                    "valor": custo_servicos.valor,
                    "porcentagem_faturamento_total": custo_servicos.porcentagem_faturamento_total
                }
            }), 200
        
        else:
            return jsonify({"message": "user não autenticado"}), 401 
