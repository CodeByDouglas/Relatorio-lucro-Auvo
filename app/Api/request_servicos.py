import requests
import json

def request_servicos_auvo(accessToken):
    """
    Faz requisição para listar serviços da API da Auvo
    
    Args:
        accessToken (str): Token de autenticação para usar no header Authorization
        
    Returns:
        dict: Resposta completa do endpoint em caso de sucesso
        None: Em caso de erro
    """
    url = "https://api.auvo.com.br/v2/services/?pageSize=999999999"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Resource with the specified apiKey does not exist
            return None
        elif response.status_code == 400:
            # Invalid options, not passing the apiKey parameter
            return None
        else:
            return None
            
    except requests.exceptions.RequestException:
        return None