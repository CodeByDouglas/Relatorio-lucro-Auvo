from app import db
from app.models.tipos_de_tarefas import Tipos_de_tarefas
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_tipos_de_tarefa(user_id, json_lista_tipos_de_tarefas):
    """
    Salva ou atualiza um único objeto tipos de tarefa no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        json_lista_tipos_de_tarefas (dict): JSON com a listagem de tipos de tarefa
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui tipos de tarefa no banco
        tipos_existentes = Tipos_de_tarefas.query.filter_by(user_id=user_id).first()
        
        if tipos_existentes:
            # Atualiza tipos de tarefa existentes
            tipos_existentes.json_lista_tipos_de_tarefas = json_lista_tipos_de_tarefas
            tipos_existentes.updated_at = datetime.now()
        else:
            # Cria novos tipos de tarefa
            novos_tipos = Tipos_de_tarefas(
                user_id=user_id,
                json_lista_tipos_de_tarefas=json_lista_tipos_de_tarefas
            )
            db.session.add(novos_tipos)
        
        db.session.commit()
        logger.info(f"Tipos de tarefa salvos/atualizados com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar tipos de tarefa para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar tipos de tarefa para usuário {user_id}: {e}")
        return False
