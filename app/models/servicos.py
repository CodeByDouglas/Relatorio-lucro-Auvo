from app import db
from datetime import datetime
import json

class Servicos(db.Model):
    __tablename__ = 'servicos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    json_lista_servicos = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o modelo User
    user = db.relationship('User', backref=db.backref('servico', lazy=True))
    
    def __init__(self, user_id, listagem_servico=None):
        self.user_id = user_id
        self.listagem_servico = listagem_servico or {}
    
    def __repr__(self):
        return f'<Servico {self.id} - User {self.user_id}>'
    
