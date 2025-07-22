from app import db
from app.models.produtos import Produtos
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_produtos(user_id, json_lista_produtos):
    """
    Salva ou atualiza um único objeto produto no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        json_lista_produtos (dict): JSON com a listagem de produtos
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Verifica se o usuário já possui um produto no banco
        produto_existente = Produtos.query.filter_by(user_id=user_id).first()
        
        if produto_existente:
            # Atualiza produto existente
            produto_existente.json_lista_produtos = json_lista_produtos
            produto_existente.updated_at = datetime.now()
        else:
            # Cria novo produto
            novo_produto = Produtos(
                user_id=user_id,
                json_lista_produtos=json_lista_produtos
            )
            db.session.add(novo_produto)
        
        db.session.commit()
        logger.info(f"Produto salvo/atualizado com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar produto para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar produto para usuário {user_id}: {e}")
        return False
