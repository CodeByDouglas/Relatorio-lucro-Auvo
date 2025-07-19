from app import db
from datetime import datetime
import json

class Tipos_de_tarefas(db.Model):
    __tablename__ = 'tipos_de_tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    json_lista_tipos_de_tarefas = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o modelo User
    user = db.relationship('User', backref=db.backref('tipos_de_tarefa', lazy=True))
    
    def __init__(self, user_id, listagem_tipos_de_tarefa=None):
        self.user_id = user_id
        self.listagem_tipos_de_tarefa = listagem_tipos_de_tarefa or {}
    
    def __repr__(self):
        return f'<Tipos_de_tarefa {self.id} - User {self.user_id}>'