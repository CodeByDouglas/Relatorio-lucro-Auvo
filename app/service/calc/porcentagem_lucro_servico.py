import logging

logger = logging.getLogger(__name__)


def calcular_porcentagem_lucro_servico(lucro_servico, lucro_total):
    """
    Calcula a porcentagem do lucro de serviços
    
    Args:
        lucro_servico (float): Lucro de serviços
        lucro_total (float): Lucro total
        
    Returns:
        float: Porcentagem do lucro de serviços
    """
    if lucro_total == 0:
        return 0.0
    return (lucro_servico / lucro_total) * 100
