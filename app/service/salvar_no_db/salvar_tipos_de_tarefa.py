from app import db
from app.models.tipos_de_tarefa import Produtos
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_tipos_de_tarefa(iduser, listagem_tipos_de_tarefa):
    """
    Salva ou atualiza um único objeto tipos de tarefa no banco de dados para um usuário específico
    
    Args:
        iduser (int): ID do usuário
        listagem_tipos_de_tarefa (dict): JSON com a listagem de tipos de tarefa
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui tipos de tarefa no banco
        tipos_existentes = Produtos.query.filter_by(user_id=iduser).first()
        
        if tipos_existentes:
            # Atualiza tipos de tarefa existentes
            tipos_existentes.listagem_tipos_de_tarefa = listagem_tipos_de_tarefa
            tipos_existentes.updated_at = datetime.now()
        else:
            # Cria novos tipos de tarefa
            novos_tipos = Produtos(
                user_id=iduser,
                listagem_tipos_de_tarefa=listagem_tipos_de_tarefa
            )
            novos_tipos.created_at = datetime.now()
            novos_tipos.updated_at = datetime.now()
            db.session.add(novos_tipos)
        
        db.session.commit()
        logger.info(f"Tipos de tarefa salvos/atualizados com sucesso para usuário {iduser}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar tipos de tarefa para usuário {iduser}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar tipos de tarefa para usuário {iduser}: {e}")
        return False
