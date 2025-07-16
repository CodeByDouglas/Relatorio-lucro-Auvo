import logging

logger = logging.getLogger(__name__)


def calcular_faturamento_total(faturamento_produto, faturamento_servico):
    """
    Calcula o faturamento total
    
    Args:
        faturamento_produto (float): Faturamento de produtos
        faturamento_servico (float): Faturamento de serviços
        
    Returns:
        float: Faturamento total
    """
    return faturamento_produto + faturamento_servico
