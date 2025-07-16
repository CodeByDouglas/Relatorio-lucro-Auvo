import logging

logger = logging.getLogger(__name__)


def calcular_porcentagem_faturamento_servico(faturamento_servico, faturamento_total):
    """
    Calcula a porcentagem do faturamento de serviços
    
    Args:
        faturamento_servico (float): Faturamento de serviços
        faturamento_total (float): Faturamento total
        
    Returns:
        float: Porcentagem do faturamento de serviços
    """
    if faturamento_total == 0:
        return 0.0
    return (faturamento_servico / faturamento_total) * 100
