from app import db
from datetime import datetime
import json

class Colaboradores(db.Model):
    __tablename__ = 'colaboradores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    json_lista_colaboradores = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com o modelo User
    user = db.relationship('User', backref=db.backref('colaboradores', lazy=True))
    
    def __init__(self, user_id, json_lista_colaboradores=None):
        self.user_id = user_id
        self.json_lista_colaboradores = json_lista_colaboradores or {}
    
    def __repr__(self):
        return f'<Colaboradores {self.id} - User {self.user_id}>'