from flask import Blueprint, render_template

dashboard_servicos_bp = Blueprint('dashboard_servicos', __name__)

@dashboard_servicos_bp.route('/dashboard_servicos')
def dashboard():
    return render_template('dashboard_servicos.html')