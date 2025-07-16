import requests
import json

def autenticar_api_auvo(api_key, api_token):
    """
    Faz autenticação na API da Auvo
    
    Args:
        api_key (str): Chave da API
        api_token (str): Token da API
        
    Returns:
        str: Access token em caso de sucesso
        None: Em caso de erro
    """
    url = f"https://api.auvo.com.br/v2/login/?apiKey={api_key}&apiToken={api_token}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('result', {}).get('accessToken')
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