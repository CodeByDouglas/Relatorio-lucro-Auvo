from app import db
from app.models.colaboradores import Colaboradores
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_colaboradores(user_id, json_lista_colaboradores):
    """
    Salva ou atualiza um único objeto colaborador no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        json_lista_colaboradores (dict): JSON com a listagem de colaboradores
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui um colaborador no banco
        colaborador_existente = Colaboradores.query.filter_by(user_id=user_id).first()
        
        if colaborador_existente:
            # Atualiza colaborador existente
            colaborador_existente.json_lista_colaboradores = json_lista_colaboradores
            colaborador_existente.updated_at = datetime.now()
        else:
            # Cria novo colaborador
            novo_colaborador = Colaboradores(
                user_id=user_id,
                json_lista_colaboradores=json_lista_colaboradores
            )
            db.session.add(novo_colaborador)
        
        db.session.commit()
        logger.info(f"Colaborador salvo/atualizado com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar colaborador para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar colaborador para usuário {user_id}: {e}")
        return False
