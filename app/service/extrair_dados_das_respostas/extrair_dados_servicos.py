import json

def extrair_lista_servicos(api_response):
    """
    Recebe o JSON da resposta do endpoint e retorna:
    [
        {
          "id-servico": "...", 
          "nome-do-servico": "..." 
        },
        ...
    ]
    
    - Mantém somente os campos essenciais.
    - Remove espaços extras no nome.
    """
    servicos = api_response["result"]["entityList"]
    lista = [
        {
                "id-servico": s["id"],
                "nome-do-servico": s["title"]
        }
        for s in servicos
    ]    
    return lista

"""
resposta_api = {
    "result": {
        "entityList": [
            {
                "id": "419384ad-705c-11eb-bf97-0aa2a285b66a",
                "title": "Preventive maintenance",
                "description": "Preventive maintenance service for the client's equipment."
            },
            {
                "id": "55555555-aaaa-bbbb-cccc-999999999999",
                "title": "Instalação",
                "description": "Serviço de instalação."
            }
        ]
    }
}

lista_servicos = extrair_lista_servicos(resposta_api)
print(lista_servicos)
# Saída:
# [
#   {'id-servico': '419384ad-705c-11eb-bf97-0aa2a285b66a', 'nome-do-servico': 'Preventive maintenance'},
#   {'id-servico': '55555555-aaaa-bbbb-cccc-999999999999', 'nome-do-servico': 'Instalação'}
# ]"""