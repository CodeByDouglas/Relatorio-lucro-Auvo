from app import db
from app.models.dados_calculados import (
    Faturamento_total, 
    Lucro_total, 
    Faturamento_produtos, 
    Faturamento_servico, 
    Lucro_produtos, 
    Lucro_servico
)
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_dados_calculados(iduser, dados_calculados):
    """
    Salva ou atualiza dados calculados no banco de dados para um usuário específico
    
    Args:
        iduser (int): ID do usuário
        dados_calculados (dict): JSON com os dados calculados
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        # Faturamento_total
        if "Faturamento_total" in dados_calculados:
            faturamento_total = Faturamento_total.query.filter_by(user_id=iduser).first()
            if faturamento_total:
                faturamento_total.valor = dados_calculados["Faturamento_total"]["valor"]
                faturamento_total.porcentagem_total_faturamento = dados_calculados["Faturamento_total"]["porcentagem_faturamento_total"]
            else:
                novo_faturamento = Faturamento_total(
                    user_id=iduser,
                    valor=dados_calculados["Faturamento_total"]["valor"],
                    porcentagem_total_faturamento=dados_calculados["Faturamento_total"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento)
        
        # Lucro_total
        if "Lucro_total" in dados_calculados:
            lucro_total = Lucro_total.query.filter_by(user_id=iduser).first()
            if lucro_total:
                lucro_total.valor = dados_calculados["Lucro_total"]["valor"]
                lucro_total.porcentagem_faturamento_total = dados_calculados["Lucro_total"]["porcentagem_faturamento_total"]
            else:
                novo_lucro = Lucro_total(
                    user_id=iduser,
                    valor=dados_calculados["Lucro_total"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Lucro_total"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_lucro)
        
        # Faturamento_produtos
        if "Faturamento_produtos" in dados_calculados:
            faturamento_produtos = Faturamento_produtos.query.filter_by(user_id=iduser).first()
            if faturamento_produtos:
                faturamento_produtos.valor = dados_calculados["Faturamento_produtos"]["valor"]
                faturamento_produtos.porcentagem_faturamento_total = dados_calculados["Faturamento_produtos"]["porcentagem_faturamento_total"]
            else:
                novo_faturamento_produtos = Faturamento_produtos(
                    user_id=iduser,
                    valor=dados_calculados["Faturamento_produtos"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Faturamento_produtos"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento_produtos)
        
        # Faturamento_servico
        if "Faturamento_servico" in dados_calculados:
            faturamento_servico = Faturamento_servico.query.filter_by(user_id=iduser).first()
            if faturamento_servico:
                faturamento_servico.valor = dados_calculados["Faturamento_servico"]["valor"]
                faturamento_servico.porcentagem_faturamento_total = dados_calculados["Faturamento_servico"]["porcentagem_faturamento_total"]
            else:
                novo_faturamento_servico = Faturamento_servico(
                    user_id=iduser,
                    valor=dados_calculados["Faturamento_servico"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Faturamento_servico"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento_servico)
        
        # Lucro_produtos
        if "Lucro_produtos" in dados_calculados:
            lucro_produtos = Lucro_produtos.query.filter_by(user_id=iduser).first()
            if lucro_produtos:
                lucro_produtos.valor = dados_calculados["Lucro_produtos"]["valor"]
                lucro_produtos.porcentagem_lucro_total = dados_calculados["Lucro_produtos"]["porcentagem_lucro_total"]
            else:
                novo_lucro_produtos = Lucro_produtos(
                    user_id=iduser,
                    valor=dados_calculados["Lucro_produtos"]["valor"],
                    porcentagem_lucro_total=dados_calculados["Lucro_produtos"]["porcentagem_lucro_total"]
                )
                db.session.add(novo_lucro_produtos)
        
        # Lucro_servico
        if "Lucro_servico" in dados_calculados:
            lucro_servico = Lucro_servico.query.filter_by(user_id=iduser).first()
            if lucro_servico:
                lucro_servico.valor = dados_calculados["Lucro_servico"]["valor"]
                lucro_servico.porcentagem_lucro_total = dados_calculados["Lucro_servico"]["porcentagem_lucro_total"]
            else:
                novo_lucro_servico = Lucro_servico(
                    user_id=iduser,
                    valor=dados_calculados["Lucro_servico"]["valor"],
                    porcentagem_lucro_total=dados_calculados["Lucro_servico"]["porcentagem_lucro_total"]
                )
                db.session.add(novo_lucro_servico)
        
        db.session.commit()
        logger.info(f"Dados calculados salvos/atualizados com sucesso para usuário {iduser}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar dados calculados para usuário {iduser}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar dados calculados para usuário {iduser}: {e}")
        return False
