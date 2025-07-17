from app import db
from app.models.produtos import Produto
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_produtos(iduser, listagem_produtos):
    """
    Salva ou atualiza um único objeto produto no banco de dados para um usuário específico
    
    Args:
        iduser (int): ID do usuário
        listagem_produtos (dict): JSON com a listagem de produtos
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui um produto no banco
        produto_existente = Produto.query.filter_by(user_id=iduser).first()
        
        if produto_existente:
            # Atualiza produto existente
            produto_existente.listagem_produtos = json.dumps(listagem_produtos)
            produto_existente.updated_at = datetime.now()
        else:
            # Cria novo produto
            novo_produto = Produto(
                user_id=iduser,
                listagem_produtos=json.dumps(listagem_produtos),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.session.add(novo_produto)
        
        db.session.commit()
        logger.info(f"Produto salvo/atualizado com sucesso para usuário {iduser}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar produto para usuário {iduser}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar produto para usuário {iduser}: {e}")
        return False
