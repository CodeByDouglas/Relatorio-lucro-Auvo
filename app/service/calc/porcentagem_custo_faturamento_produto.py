def calcular_porcentagem_custo_faturamento_produto(faturamento_produtos, custo_produtos):
    """
    Calcula a porcentagem que o custo de produtos representa do faturamento de produtos.
    
    Args:
        faturamento_produtos (float): Valor total do faturamento de produtos
        custo_produtos (float): Valor total do custo de produtos
    
    Returns:
        float: Porcentagem do custo em relação ao faturamento (0-100)
    """
    try:
        # Verifica se o faturamento é maior que zero para evitar divisão por zero
        if faturamento_produtos <= 0:
            return 0.0
        
        # Calcula a porcentagem
        porcentagem = (custo_produtos / faturamento_produtos) * 100
        
        # Retorna a porcentagem limitada a 2 casas decimais
        return round(porcentagem, 2)
        
    except (TypeError, ValueError, ZeroDivisionError):
        # Retorna 0 em caso de erro
        return 0.0
