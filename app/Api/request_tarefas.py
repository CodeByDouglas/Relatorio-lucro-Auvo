import requests
import json
from urllib.parse import urlencode

def request_tarefas_auvo(token_autenticacao, page, start_date, end_date, status, id_user_to, type):
    """
    Faz requisição para listar tarefas da API da Auvo
    
    Args:
        token_autenticacao (str): Token de autenticação para usar no header Authorization
        page (int): Número da página
        start_date (str): Data de início no formato yyyy-mm-dd
        end_date (str): Data de fim no formato yyyy-mm-dd
        status (int): Status da tarefa
        id_user_to (int): ID do usuário destinatário
        type (int): Tipo da tarefa
        
    Returns:
        dict: Resposta completa do endpoint em caso de sucesso
        None: Em caso de erro
    """
    # Construir o objeto paramFilter
    param_filter = {
        "startDate": start_date,
        "endDate": end_date,
        "status": status,
        "idUserTo": id_user_to,
        "type": type
    }
    
    # Construir a URL com os parâmetros
    base_url = "https://api.auvo.com.br/v2/tasks/"
    params = {
        "page": page,
        "pageSize": 100,
        "paramFilter": json.dumps(param_filter)
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token_autenticacao}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Tarefas não encontradas
            return 404
        elif response.status_code == 401:
            # User não autenticado
            return None
        else:
            return None
            
    except requests.exceptions.RequestException:
        return None