import logging

logger = logging.getLogger(__name__)


def calcular_lucro_total(lucro_produto, lucro_servico):
    """
    Calcula o lucro total
    
    Args:
        lucro_produto (float): Lucro de produtos
        lucro_servico (float): Lucro de serviços
        
    Returns:
        float: Lucro total
    """
    return lucro_produto + lucro_servico
