from flask import Blueprint, render_template
from app.controller.login.logar import login_bp as controller_login_bp

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    return render_template('login.html')
