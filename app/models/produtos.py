from app import db
from datetime import datetime
import json

class Produtos(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    json_lista_produtos = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o modelo User
    user = db.relationship('User', backref=db.backref('produtos', lazy=True))
    
    def __init__(self, user_id, json_lista_produtos=None):
        self.user_id = user_id
        self.json_lista_produtos = json_lista_produtos or {}
    
    def __repr__(self):
        return f'<Produtos {self.id} - User {self.user_id}>'
    
