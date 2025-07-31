import logging
from .faturamento_total import calcular_faturamento_total
from .lucro_produto import calcular_lucro_produto
from .lucro_servico import calcular_lucro_servico
from .lucro_total import calcular_lucro_total
from .porcentagem_faturamento_produto import calcular_porcentagem_faturamento_produto
from .porcentagem_faturamento_servico import calcular_porcentagem_faturamento_servico
from .porcentagem_lucro_produto import calcular_porcentagem_lucro_produto
from .porcentagem_lucro_servico import calcular_porcentagem_lucro_servico
from .porcentagem_lucro_faturamento import calcular_porcentagem_lucro_faturamento
from .porcentagem_custo_faturamento_produto import calcular_porcentagem_custo_faturamento_produto
from .porcentagem_custo_faturamento_servico import calcular_porcentagem_custo_faturamento_servico
from .porcentagem_custo_faturamento import calcular_porcentagem_custo_faturamento
from .custo_total import calcular_custo_total

logger = logging.getLogger(__name__)


def calcular_todos_os_valores(faturamento_produto, faturamento_servico, custo_produto, custo_servico):
    """
    Calcula todos os valores financeiros de uma vez
    
    Args:
        faturamento_produto (float): Faturamento de produtos
        faturamento_servico (float): Faturamento de serviços
        custo_produto (float): Custo dos produtos
        
    Returns:
        dict: Dicionário com todos os valores calculados
    """
    
    # Cálculos básicos
    faturamento_total = calcular_faturamento_total(faturamento_produto, faturamento_servico)
    lucro_produto = calcular_lucro_produto(faturamento_produto, custo_produto)
    lucro_servico = calcular_lucro_servico(faturamento_servico, custo_servico)
    lucro_total = calcular_lucro_total(lucro_produto, lucro_servico)
    
    # Porcentagens
    porc_faturamento_produto = calcular_porcentagem_faturamento_produto(faturamento_produto, faturamento_total)
    porc_faturamento_servico = calcular_porcentagem_faturamento_servico(faturamento_servico, faturamento_total)
    porc_lucro_produto = calcular_porcentagem_lucro_produto(lucro_produto, lucro_total)
    porc_lucro_servico = calcular_porcentagem_lucro_servico(lucro_servico, lucro_total)
    porc_lucro_faturamento = calcular_porcentagem_lucro_faturamento(lucro_total, faturamento_total)
    porc_custo_produto = calcular_porcentagem_custo_faturamento_produto(faturamento_produto, custo_produto)
    porc_custo_servico = calcular_porcentagem_custo_faturamento_servico(faturamento_servico, custo_servico)
    custo_total = calcular_custo_total(custo_produto, custo_servico)
    porc_custo_total = calcular_porcentagem_custo_faturamento(faturamento_total, custo_total)
    dado_calculados = {
        'Faturamento_total': {
            'valor': faturamento_total,
            'porcentagem_faturamento_total': 100.0  # Faturamento total sempre é 100% de si mesmo
        },
        'Lucro_total': {
            'valor': lucro_total,
            'porcentagem_faturamento_total': porc_lucro_faturamento
        },
        'Faturamento_produtos': {
            'valor': faturamento_produto,
            'porcentagem_faturamento_total': porc_faturamento_produto
        },
        'Faturamento_servicos': {
            'valor': faturamento_servico,
            'porcentagem_faturamento_total': porc_faturamento_servico
        },
        'Lucro_produtos': {
            'valor': lucro_produto,
            'porcentagem_lucro_total': porc_lucro_produto
        },
        'Lucro_servicos': {
            'valor': lucro_servico,
            'porcentagem_lucro_total': porc_lucro_servico
        },
        'Custo_produtos': {
            'valor': custo_produto,
            'porcentagem_faturamento_total': porc_custo_produto
        },
        'Custo_servicos': {
            'valor': custo_servico,
            'porcentagem_faturamento_total': porc_custo_servico
        },
        'Custo_total': {
            'valor': custo_total,
            'porcentagem_faturamento_total': porc_custo_total
        }
    }
    
    return dado_calculados
