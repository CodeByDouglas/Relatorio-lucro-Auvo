from flask import request, jsonify
from flask import Blueprint
from app.controller.login.check_auth import check_auth
from app.models.dados_calculados import  Faturamento_produtos, Lucro_produtos, Custo_produtos
from app.models.user import User
from app.controller.dashboard.dashboard_geral import dashboard_controller_bp

@dashboard_controller_bp.route('/dashboard_produtos', methods=['GET'])
def dados_dashboard_produtos():
        api_key = request.args.get('api_key')

        auth = check_auth(api_key)

        if auth[0]: 
            user = User.query.filter_by(api_key=api_key).first()
            user_id = user.id
            
            faturamento_produtos = Faturamento_produtos.query.filter_by(user_id=user_id).first()
            lucro_produtos = Lucro_produtos.query.filter_by(user_id=user_id).first()
            custo_produtos = Custo_produtos.query.filter_by(user_id=user_id).first()
            
            # Calcular a porcentagem do lucro em relação ao faturamento de produtos.
            porcentagem_lucro = 0
            if faturamento_produtos.valor > 0:
                porcentagem_lucro = (lucro_produtos.valor / faturamento_produtos.valor) * 100
            
            return jsonify({
                
                "faturamento_produtos": {
                    "valor": faturamento_produtos.valor,
                    "porcentagem_faturamento_total": 100
                },
                
                "lucro_produtos": {
                    "valor": lucro_produtos.valor,
                    "porcentagem_lucro_total": porcentagem_lucro
                },
                
                "custo_produtos": {
                    "valor": custo_produtos.valor,
                    "porcentagem_faturamento_total": custo_produtos.porcentagem_faturamento_total
                }
            }), 200
        
        else:
            return jsonify({"message": "user não autenticado"}), 401 
