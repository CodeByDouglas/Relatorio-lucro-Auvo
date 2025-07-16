from flask import Blueprint, jsonify, request, render_template
from app import db
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página inicial"""
    return render_template('index.html')

@main.route('/health')
def health():
    """Endpoint de saúde da aplicação"""
    return jsonify({
        'status': 'success',
        'message': 'Aplicação Flask rodando com sucesso!',
        'database': 'SQLite conectado'
    })

@main.route('/users', methods=['GET'])
def get_users():
    """Retorna todos os usuários"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@main.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Username e email são obrigatórios'}), 400
    
    try:
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar usuário. Talvez username ou email já existam.'}), 400

@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna um usuário específico"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deleta um usuário"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso'})
