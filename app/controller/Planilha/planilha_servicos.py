from flask import Blueprint, request, jsonify, send_file
from app.controller.login.check_auth import check_auth
from app.models.user import User


planilha_servicos_bp = Blueprint('planilha_servicos', __name__, url_prefix='/gerar_planilha')

@planilha_servicos_bp.route('/servico', methods=['GET'])
def gerar_planilha_servico():
    api_key = request.args.get('api_key')
    auth = check_auth(api_key)

    if not auth[0]:
        return jsonify({"message": "user não autenticado"}), 401

    user = User.query.filter_by(api_key=api_key).first()
    user_id = user.id

    # Gerar a planilha Excel
    from app.service.gerar_planilhas.planilha_servicos import gerar_planilha_excel_servico
    temp_file_path = gerar_planilha_excel_servico(user_id)

    return send_file(temp_file_path, as_attachment=True, download_name='Relatorio_de_Lucro_Servico.xlsx'), 200
