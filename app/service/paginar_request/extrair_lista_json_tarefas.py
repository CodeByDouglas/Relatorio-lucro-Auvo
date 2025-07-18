from app.service.extrair_dados.extrair_json_tarefas import extrair_json_tarefas


def extrair_lista_json_tarefas(lista_respostas, allowed_products, allowed_services):
    """
    Função que processa uma lista de respostas e formata cada uma usando extrair_json_tarefas
    
    Args:
        lista_respostas (list): Lista de respostas retornada pela função paginar_respostas_request_tarefas
        allowed_products (list): Array com produtos permitidos
        allowed_services (list): Array com serviços permitidos
        
    Returns:
        list: Array com todas as respostas formatadas
    """
    respostas_formatadas = []
    
    for resposta in lista_respostas:
        # Chama extrair_json_tarefas para cada resposta
        resultado_formatado = extrair_json_tarefas(
            api_response=resposta,
            allowed_products=allowed_products,
            allowed_services=allowed_services
        )
        
        # Adiciona a resposta formatada ao array
        respostas_formatadas.append(resultado_formatado)
    
    return respostas_formatadas
