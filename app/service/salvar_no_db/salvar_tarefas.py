from app import db
from app.models.tarefas import Produtos
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_tarefas(iduser, listagem_tarefas):
    """
    Salva ou atualiza um único objeto tarefas no banco de dados para um usuário específico
    
    Args:
        iduser (int): ID do usuário
        listagem_tarefas (dict): JSON com a listagem de tarefas
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui tarefas no banco
        tarefas_existentes = Produtos.query.filter_by(user_id=iduser).first()
        
        if tarefas_existentes:
            # Atualiza tarefas existentes
            tarefas_existentes.listagem_tarefas = listagem_tarefas
            tarefas_existentes.updated_at = datetime.now()
        else:
            # Cria novas tarefas
            novas_tarefas = Produtos(
                user_id=iduser,
                listagem_tarefas=listagem_tarefas
            )
            novas_tarefas.created_at = datetime.now()
            novas_tarefas.updated_at = datetime.now()
            db.session.add(novas_tarefas)
        
        db.session.commit()
        logger.info(f"Tarefas salvas/atualizadas com sucesso para usuário {iduser}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar tarefas para usuário {iduser}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar tarefas para usuário {iduser}: {e}")
        return False
