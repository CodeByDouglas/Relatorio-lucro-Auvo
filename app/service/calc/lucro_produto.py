import logging

logger = logging.getLogger(__name__)


def calcular_lucro_produto(faturamento_produto, custo_produto):
    """
    Calcula o lucro de produtos
    
    Args:
        faturamento_produto (float): Faturamento de produtos
        custo_produto (float): Custo dos produtos
        
    Returns:
        float: Lucro de produtos
    """
    return faturamento_produto - custo_produto
