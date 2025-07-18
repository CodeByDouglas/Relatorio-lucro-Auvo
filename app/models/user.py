from app import db
from datetime import datetime
import uuid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), nullable=True)
    token_autenticacao = db.Column(db.String(255), nullable=True)
    horario_da_ultima_autenticacao = db.Column(db.DateTime, nullable=True)
    
    
    def __repr__(self):
        return f'<User {self.username}>'
    
