from app.service.calc.custo_produtos import calcular_custo_produtos
from app.service.calc.lucro_servico import calcular_lucro_servico
from app.service.calc.lucro_produto import calcular_lucro_produto
from app.service.calc.lucro_total import calcular_lucro_total
from app.service.calc.faturamento_total import calcular_faturamento_total

def calcular_todos_os_dados_tarefa_individual(lista_tarefas, lista_produtos):
    """
    Processa uma lista de tarefas e calcula os lucros individuais para cada tarefa.

    Parâmetros:
        lista_tarefas: Lista de dicts com dados das tarefas
        lista_produtos: Lista de dicts com dados dos produtos (id-produto, nome-do-produto, custo-do-produto)

    Retorna:
        Lista de tarefas com campos adicionais: lucro-servicos, lucro-produto, lucro-total, faturamento-total
    """
    
    tarefas_processadas = []
    for tarefa in lista_tarefas:
        tarefa_processada = tarefa.copy()

        faturamento_servicos = tarefa.get('faturamento-servicos', 0)
        faturamento_produtos = tarefa.get('faturamento-produtos', 0)
        produtos_ids = tarefa.get('produtos', [])
        custo_total_produtos = calcular_custo_produtos(produtos_ids, lista_produtos)

        lucro_servicos = calcular_lucro_servico(faturamento_servicos)
        tarefa_processada['lucro-servicos'] = lucro_servicos

        lucro_produto = calcular_lucro_produto(faturamento_produtos, custo_total_produtos)
        tarefa_processada['lucro-produto'] = lucro_produto

        faturamento_total = calcular_faturamento_total(faturamento_produtos, faturamento_servicos)
        tarefa_processada['faturamento-total'] = faturamento_total

        lucro_total = calcular_lucro_total(lucro_produto, lucro_servicos)
        tarefa_processada['lucro-total'] = lucro_total

        tarefas_processadas.append(tarefa_processada)
    return tarefas_processadas
