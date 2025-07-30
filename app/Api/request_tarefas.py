import requests
import json
from urllib.parse import urlencode

def request_tarefas_completa(accessToken, start_date, end_date, type, status, id_colaborador):
    """
    Requisita todas as tarefas da API Auvo dentro de um intervalo de datas com paginação automática.

    Args:
        accessToken (str): Token de autenticação Bearer
        start_date (str): Data inicial (formato yyyy-mm-dd)
        end_date (str): Data final (formato yyyy-mm-dd)
        tipo_tarefa (int): ID do tipo de tarefa

    Returns:
        list: Lista contendo todas as tarefas obtidas
    """
    respostas = []
    current_page = 1

    while True:
        param_filter = {
            "startDate": start_date,
            "endDate": end_date,
               
        }
        
        if type is not None:
            param_filter["type"] = type

        if status is not None:
            param_filter["status"] = status

        if id_colaborador is not None:
            param_filter["idUserTo"] = id_colaborador
        

        base_url = "https://api.auvo.com.br/v2/tasks/"
        params = {
            "page": current_page,
            "pageSize": 100,
            "paramFilter": json.dumps(param_filter)
        } 
        print(param_filter)

        url = f"{base_url}?{urlencode(params)}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {accessToken}'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                respostas.append(data)

                total_items = data.get("result", {}).get("pagedSearchReturnData", {}).get("totalItems", 0)

                if total_items < 100:
                    break
                current_page += 1
            
            elif (response.status_code == 404) and (current_page == 1):
                print("Tarefas não encontradas")
                break
            elif (response.status_code == 404):
                break
            else:
                print(f"Erro ao obter tarefas. Código {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            break

    return respostas
