import logging

logger = logging.getLogger(__name__)


def calcular_porcentagem_lucro_produto(lucro_produto, lucro_total):
    """
    Calcula a porcentagem do lucro de produtos
    
    Args:
        lucro_produto (float): Lucro de produtos
        lucro_total (float): Lucro total
        
    Returns:
        float: Porcentagem do lucro de produtos
    """
    if lucro_total == 0:
        return 0.0
    return (lucro_produto / lucro_total) * 100
