def calcular_porcentagem_custo_faturamento(faturamento_total, custo_total):
    """
    Calcula a porcentagem que o custo total representa do faturamento total.

    Args:
        faturamento_total (float): Valor total do faturamento
        custo_total (float): Valor total do custo

    Returns:
        float: Porcentagem do custo em relação ao faturamento (0-100)
    """
    try:
        # Verifica se o faturamento é maior que zero para evitar divisão por zero
        if faturamento_total <= 0:
            return 0.0

        # Calcula a porcentagem
        porcentagem = (custo_total / faturamento_total) * 100

        # Retorna a porcentagem limitada a 2 casas decimais
        return round(porcentagem, 2)

    except (TypeError, ValueError, ZeroDivisionError):
        # Retorna 0 em caso de erro
        return 0.0
