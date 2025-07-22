from app import db
from app.models.tarefas import Tarefas
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_tarefas(user_id, json_lista_tarefas):
    """
    Salva ou atualiza um único objeto tarefas no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        json_lista_tarefas (dict): JSON com a listagem de tarefas
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui tarefas no banco
        tarefas_existentes = Tarefas.query.filter_by(user_id=user_id).first()
        
        if tarefas_existentes:
            # Atualiza tarefas existentes
            tarefas_existentes.json_lista_tarefas = json_lista_tarefas
            tarefas_existentes.updated_at = datetime.now()
        else:
            # Cria novas tarefas
            novas_tarefas = Tarefas(
                user_id=user_id,
                json_lista_tarefas=json_lista_tarefas
            )
            db.session.add(novas_tarefas)
        
        db.session.commit()
        logger.info(f"Tarefas salvas/atualizadas com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar tarefas para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar tarefas para usuário {user_id}: {e}")
        return False
