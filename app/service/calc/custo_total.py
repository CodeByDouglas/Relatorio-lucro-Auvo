def calcular_custo_total(custo_produtos, custo_servicos):
    """
    Calcula o custo total somando o custo de produtos e o custo de serviços.

    Args:
        custo_produtos (float): Valor total do custo de produtos
        custo_servicos (float): Valor total do custo de serviços

    Returns:
        float: Valor total do custo (produtos + serviços)
    """
    try:
        # Converte para float e soma os custos
        custo_total = float(custo_produtos) + float(custo_servicos)
        
        # Retorna o valor limitado a 2 casas decimais
        return round(custo_total, 2)
        
    except (TypeError, ValueError):
        # Retorna 0 em caso de erro na conversão
        return 0.0
