from app.Api.request_tarefas import request_tarefas_auvo


def request_tarefas_paginadas(data_inicial, data_final, id_tipo_de_tarefa, status, page, token_autenticacao):
    """
    Função para paginar respostas da API de tarefas da Auvo
    
    Args:
        data_inicial (str): Data inicial no formato yyyy-mm-dd
        data_final (str): Data final no formato yyyy-mm-dd
        id_tipo_de_tarefa (int): ID do tipo de tarefa
        status (int): Status da tarefa
        page (int): Número da página inicial
        token_autenticacao (str): Token de autenticação
        
    Returns:
        list: Array com todos os JSONs obtidos durante as requisições
        str: "erro" em caso de falha
    """
    respostas = []
    current_page = page
    
    while True:
        # Chama a função request_tarefas_auvo
        resultado = request_tarefas_auvo(
            token_autenticacao=token_autenticacao,
            page=current_page,
            start_date=data_inicial,
            end_date=data_final,
            status=status,
            type=id_tipo_de_tarefa
        )
        
        # Verifica se retornou None (erro)
        if resultado is None:
            return "erro"
        
        # Verifica se retornou 404 (não encontrado)
        if resultado == 404:
            return respostas
        
        # Se chegou aqui, recebeu um JSON válido
        respostas.append(resultado)
        
        # Verifica o totalItems
        total_items = resultado.get("result", {}).get("pagedSearchReturnData", {}).get("totalItems", 0)
        
        # Se totalItems <= 99, finaliza e retorna o array
        if total_items <= 99:
            return respostas
        
        # Se totalItems == 100, incrementa a página e continua
        if total_items == 100:
            current_page += 1
        else:
            # Se não for 100 nem <= 99, finaliza
            return respostas
