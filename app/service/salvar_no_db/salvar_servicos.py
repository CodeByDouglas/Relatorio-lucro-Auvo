from app import db
from app.models.serviço import Produtos
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_servicos(iduser, listagem_servico):
    """
    Salva ou atualiza um único objeto serviço no banco de dados para um usuário específico
    
    Args:
        iduser (int): ID do usuário
        listagem_servico (dict): JSON com a listagem de serviços
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui um serviço no banco
        servico_existente = Produtos.query.filter_by(user_id=iduser).first()
        
        if servico_existente:
            # Atualiza serviço existente
            servico_existente.listagem_servico = listagem_servico
            servico_existente.updated_at = datetime.now()
        else:
            # Cria novo serviço
            novo_servico = Produtos(
                user_id=iduser,
                listagem_servico=listagem_servico
            )
            novo_servico.created_at = datetime.now()
            novo_servico.updated_at = datetime.now()
            db.session.add(novo_servico)
        
        db.session.commit()
        logger.info(f"Serviço salvo/atualizado com sucesso para usuário {iduser}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar serviço para usuário {iduser}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar serviço para usuário {iduser}: {e}")
        return False
