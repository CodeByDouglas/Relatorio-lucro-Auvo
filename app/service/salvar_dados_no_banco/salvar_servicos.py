from app import db
from app.models.servicos import Servicos
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_servicos(user_id, json_lista_servicos):
    """
    Salva ou atualiza um único objeto serviço no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        json_lista_servicos (dict): JSON com a listagem de serviços
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui um serviço no banco
        servico_existente = Servicos.query.filter_by(user_id=user_id).first()
        
        if servico_existente:
            # Atualiza serviço existente
            servico_existente.json_lista_servicos = json_lista_servicos
            servico_existente.updated_at = datetime.now()
        else:
            # Cria novo serviço
            novo_servico = Servicos(
                user_id=user_id,
                json_lista_servicos=json_lista_servicos
            )
            db.session.add(novo_servico)
        
        db.session.commit()
        logger.info(f"Serviço salvo/atualizado com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar serviço para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar serviço para usuário {user_id}: {e}")
        return False
