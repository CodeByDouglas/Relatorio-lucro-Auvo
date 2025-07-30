from app.service.calc.custo_produtos import calcular_custo_produtos
from app.service.calc.custo_servicos import calcular_custo_servicos, converter_tempo_para_minutos
from app.service.calc.lucro_servico import calcular_lucro_servico
from app.service.calc.lucro_produto import calcular_lucro_produto
from app.service.calc.lucro_total import calcular_lucro_total
from app.service.calc.faturamento_total import calcular_faturamento_total

def calcular_todos_os_dados_tarefa_individual(lista_tarefas, lista_produtos, lista_colaboradores):
    """
    Processa uma lista de tarefas e calcula os lucros individuais para cada tarefa.

    Parâmetros:
        lista_tarefas: Lista de dicts com dados das tarefas
        lista_produtos: Lista de dicts com dados dos produtos (id-produto, nome-do-produto, custo-do-produto)
        lista_colaboradores: Lista de dicts com dados dos colaboradores (id-colaborador, nome-do-colaborador, Valor-da-hora)

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

        # Calcular custo de serviços para esta tarefa individual
        servicos_tarefa = tarefa.get('serviços', [])
        if servicos_tarefa:
            # Criar lista com apenas esta tarefa para usar a função calcular_custo_servicos
            lista_tarefa_individual = [tarefa]
            custo_servicos_tarefa = calcular_custo_servicos(lista_tarefa_individual, lista_colaboradores, servicos_tarefa)
        else:
            custo_servicos_tarefa = 0.0

        lucro_servicos = calcular_lucro_servico(faturamento_servicos, custo_servicos_tarefa)
        tarefa_processada['lucro-servicos'] = lucro_servicos

        lucro_produto = calcular_lucro_produto(faturamento_produtos, custo_total_produtos)
        tarefa_processada['lucro-produto'] = lucro_produto

        faturamento_total = calcular_faturamento_total(faturamento_produtos, faturamento_servicos)
        tarefa_processada['faturamento-total'] = faturamento_total

        lucro_total = calcular_lucro_total(lucro_produto, lucro_servicos)
        tarefa_processada['lucro-total'] = lucro_total

        tarefas_processadas.append(tarefa_processada)
    return tarefas_processadas



