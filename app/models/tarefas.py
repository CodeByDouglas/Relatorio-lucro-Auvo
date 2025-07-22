from app import db
from datetime import datetime
import json

class Tarefas(db.Model):
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    json_lista_tarefas = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o modelo User
    user = db.relationship('User', backref=db.backref('tarefas', lazy=True))
    
    def __init__(self, user_id, json_lista_tarefas=None):
        self.user_id = user_id
        self.json_lista_tarefas = json_lista_tarefas or {}
    
    def __repr__(self):
        return f'<Tarefas {self.id} - User {self.user_id}>'