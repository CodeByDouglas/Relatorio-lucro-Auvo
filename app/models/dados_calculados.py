from app import db
from datetime import datetime

class Faturamento_total(db.Model):
    __tablename__ = 'faturamento_total'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_total_faturamento = db.Column(db.Float, nullable=False)

class Lucro_total(db.Model):
    __tablename__ = 'lucro_total'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_faturamento_total = db.Column(db.Float, nullable=False)

class Faturamento_produtos(db.Model):
    __tablename__ = 'faturamento_produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_faturamento_total = db.Column(db.Float, nullable=False)

class Faturamento_servico(db.Model):
    __tablename__ = 'faturamento_servico'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_faturamento_total = db.Column(db.Float, nullable=False)

class Lucro_produtos(db.Model):
    __tablename__ = 'lucro_produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_lucro_total = db.Column(db.Float, nullable=False)

class Lucro_servico(db.Model):
    __tablename__ = 'lucro_servico'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    porcentagem_lucro_total = db.Column(db.Float, nullable=False)