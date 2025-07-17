from flask import Blueprint, render_template

relatorio_detalhado_bp = Blueprint('relatorio_detalhado', __name__)

@relatorio_detalhado_bp.route('/relatorio_detalhado')
def relatorio_detalhado():
    return render_template('relatorio_detalhado.html')
