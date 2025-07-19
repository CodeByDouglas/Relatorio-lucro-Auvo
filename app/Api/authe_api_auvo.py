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
            print(data)
            result = data.get('result')
            authenticated = result.get('authenticated')
            if authenticated == True:
                expiration = result.get('expiration')
                accessToken = result.get('accessToken')
                return response.status_code, authenticated, expiration, accessToken #Autenticado com sucesso
            else:
                return response.status_code, authenticated #Requisição recebida dados incorretos
        elif response.status_code == 400:
            return response.status_code, #api_key e api_token são necessários
        elif response.status_code == 500:
            return response.status_code #Erro interno
        else:
            return response.status_code, None #Erro desconhecido 
            
    except requests.exceptions.RequestException:
        return None, None