def extrair_lista_colaboradores(api_response):
    """
    Recebe o JSON completo vindo do endpoint e devolve **apenas** uma lista de dicts:

    [
      {
        "id-colaborador": "...",
        "nome-do-colaborador": "...",
        "Valor-da-hora": "..."
      },
      ...
    ]

    - Mantém somente os campos essenciais.
    - Remove espaços extras no nome.
    """
    colaboradores = api_response["result"]["entityList"]
    lista = [
        {
            "id-colaborador": str(c["userID"]),
            "nome-do-colaborador": c.get("name", "").strip(),
            "Valor-da-hora": str(c.get("hourValue", "0"))
        }
        for c in colaboradores
    ]
    return lista


"""
resposta_api = {
    "result": {
        "entityList": [
            {
                "userID": 201975,
                "name": "Douglas",
                "hourValue": 1000.0
            },
            {
                "userID": 198544,
                "name": "GABRIELA - TESTE",
                "hourValue": 0.0
            }
        ]
    }
}

lista_colaboradores = extrair_lista_colaboradores(resposta_api)
print(lista_colaboradores)
# Saída:
# [
#   {'id-colaborador': '201975', 'nome-do-colaborador': 'Douglas', 'Valor-da-hora': '1000.0'},
#   {'id-colaborador': '198544', 'nome-do-colaborador': 'GABRIELA - TESTE', 'Valor-da-hora': '0.0'}
# ]"""
