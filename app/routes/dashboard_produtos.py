from flask import Blueprint, render_template

dashboard_produtos_bp = Blueprint('dashboard_produtos', __name__)

@dashboard_produtos_bp.route('/dashboard_produtos')
def dashboard():
    return render_template('dashboard_produtos.html')