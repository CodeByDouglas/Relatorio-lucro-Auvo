import logging

logger = logging.getLogger(__name__)


def calcular_lucro_servico(faturamento_servico, custo_servico):
    """
    Calcula o lucro de serviços
    
    Args:
        faturamento_servico (float): Faturamento de serviços
        custo_servico (float): Custo dos serviços
        
    Returns:
        float: Lucro de serviços
    """
    return faturamento_servico - custo_servico
