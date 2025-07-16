import logging

logger = logging.getLogger(__name__)


def calcular_porcentagem_lucro_faturamento(lucro_total, faturamento_total):
    """
    Calcula a porcentagem do lucro sobre o faturamento (margem de lucro)
    
    Args:
        lucro_total (float): Lucro total
        faturamento_total (float): Faturamento total
        
    Returns:
        float: Porcentagem do lucro sobre o faturamento
    """
    if faturamento_total == 0:
        return 0.0
    return (lucro_total / faturamento_total) * 100
