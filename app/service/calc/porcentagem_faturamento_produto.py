import logging

logger = logging.getLogger(__name__)


def calcular_porcentagem_faturamento_produto(faturamento_produto, faturamento_total):
    """
    Calcula a porcentagem do faturamento de produtos
    
    Args:
        faturamento_produto (float): Faturamento de produtos
        faturamento_total (float): Faturamento total
        
    Returns:
        float: Porcentagem do faturamento de produtos
    """
    if faturamento_total == 0:
        return 0.0
    return (faturamento_produto / faturamento_total) * 100
