def calcular_porcentagem_custo_faturamento_servico(faturamento_servicos, custo_servicos):
    """
    Calcula a porcentagem que o custo de serviços representa do faturamento de serviços.
    
    Args:
        faturamento_servicos (float): Valor total do faturamento de serviços
        custo_servicos (float): Valor total do custo de serviços
    
    Returns:
        float: Porcentagem do custo em relação ao faturamento (0-100)
    """
    try:
        # Verifica se o faturamento é maior que zero para evitar divisão por zero
        if faturamento_servicos <= 0:
            return 0.0
        
        # Calcula a porcentagem
        porcentagem = (custo_servicos / faturamento_servicos) * 100
        
        # Retorna a porcentagem limitada a 2 casas decimais
        return round(porcentagem, 2)
        
    except (TypeError, ValueError, ZeroDivisionError):
        # Retorna 0 em caso de erro
        return 0.0
