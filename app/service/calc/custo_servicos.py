def calcular_custo_servicos(lista_tarefas, lista_colaboradores, filtro_listagem_id_servicos):
    """
    Calcula o custo total da mão de obra baseado nos serviços, colaboradores e tempo de serviço.
    
    Args:
        lista_tarefas (list): Lista de tarefas com informações de serviços, colaboradores e tempo
        lista_colaboradores (list): Lista de colaboradores com valores por hora
        filtro_listagem_id_servicos (list): Lista de IDs de serviços a considerar
        
    Returns:
        float: Valor total do custo da mão de obra
    """
    
    # Criar dicionário para busca rápida de colaboradores por ID
    colaboradores_dict = {}
    for colaborador in lista_colaboradores:
        colaboradores_dict[colaborador["id-colaborador"]] = {
            "nome": colaborador["nome-do-colaborador"],
            "valor_hora": float(colaborador["Valor-da-hora"])
        }
    
    # Criar set para busca rápida de IDs de serviços
    servicos_filtro = set(filtro_listagem_id_servicos)
    
    custo_total = 0.0
    
    for tarefa in lista_tarefas:
        # Verificar se a tarefa possui serviços que estão no filtro
        servicos_tarefa = set(tarefa.get("serviços", []))
        
        # Se há interseção entre os serviços da tarefa e o filtro
        if servicos_tarefa.intersection(servicos_filtro):
            id_colaborador = str(tarefa.get("id-do-colaborador", ""))
            tempo_servico = tarefa.get("tempo-de-serviço", "")
            
            # Verificar se o colaborador existe e se há tempo de serviço
            if id_colaborador in colaboradores_dict and tempo_servico:
                valor_hora = colaboradores_dict[id_colaborador]["valor_hora"]
                
                # Converter tempo de serviço para minutos
                tempo_minutos = converter_tempo_para_minutos(tempo_servico)
                
                if tempo_minutos > 0:
                    # Calcular custo: (valor_hora / 60) * tempo_minutos
                    custo_tarefa = (valor_hora / 60) * tempo_minutos
                    custo_total += custo_tarefa
    
    return custo_total


def converter_tempo_para_minutos(tempo_str):
    """
    Converte string de tempo no formato "HH:MM:SS" para minutos.
    
    Args:
        tempo_str (str): String de tempo no formato "HH:MM:SS"
        
    Returns:
        int: Tempo em minutos
    """
    if not tempo_str or tempo_str == "":
        return 0
    
    try:
        # Dividir a string por ":"
        partes = tempo_str.split(":")
        
        if len(partes) == 3:  # Formato HH:MM:SS
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])
            
            # Converter tudo para minutos
            total_minutos = (horas * 60) + minutos + (segundos / 60)
            return total_minutos
        elif len(partes) == 2:  # Formato MM:SS
            minutos = int(partes[0])
            segundos = int(partes[1])
            
            total_minutos = minutos + (segundos / 60)
            return total_minutos
        else:
            return 0
            
    except (ValueError, IndexError):
        return 0


"""
# Exemplo de uso:

lista_tarefas = [
    {
        "id-da-tarefa": 61367639,
        "nome-do-cliente": "Condomínio Auvo",
        "data-da-tarefa": "2025-07-29T09:00:00",
        "tipo-da-tarefa": 182794,
        "id-do-colaborador": 175745,
        "tempo-de-serviço": "01:30:00",
        "produtos": ["1f58d4ed-610d-11f0-ba85-0a44e9849753"],
        "serviços": ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462"],
        "faturamento-produtos": 500,
        "faturamento-servicos": 250,
        "lucro-servicos": 250,
        "lucro-produto": 250,
        "faturamento-total": 750,
        "lucro-total": 500
    }
]

lista_colaboradores = [
    {
        "id-colaborador": "175745",
        "nome-do-colaborador": "Silva Adm",
        "Valor-da-hora": "0.0"
    }
]

filtro_listagem_id_servicos = ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462"]

custo_total = calcular_custo_servicos(lista_tarefas, lista_colaboradores, filtro_listagem_id_servicos)
print(f"Custo total da mão de obra: R$ {custo_total:.2f}")
"""
