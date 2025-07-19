def extrair_lista_produtos(api_response):
    """
    Recebe o JSON completo vindo do endpoint e devolve **apenas** uma lista de dicts:

    [
      {
        "id-produto": "...",
        "nome-do-produto": "...",
        "custo-do-produto": "..."
      },
      ...
    ]

    - Mantém somente os campos essenciais.
    - Remove espaços extras no nome.
    """
    produtos = api_response["result"]["entityList"]
    lista = [
        {
            "id-produto": p["productId"],
            "nome-do-produto": p.get("name", "").strip(),
            "custo-do-produto": p.get("unitaryCost", "0")
        }
        for p in produtos
    ]
    return lista


"""
resposta_api = {
    "result": {
        "entityList": [
            {
                "productId": "63867f52-b262-410a-a409-cc25ba92ded1",
                "name": "Produto X ",
                "unitaryCost": "6,00"
            },
            {
                "productId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "name": "Outro Produto",
                "unitaryCost": "10,50"
            }
        ]
    }
}

lista_produtos = extrair_lista_produtos(resposta_api)
print(lista_produtos)
# Saída:
# [
#   {'id-produto': '63867f52-b262-410a-a409-cc25ba92ded1', 'nome-do-produto': 'Produto X', 'custo-do-produto': '6,00'},
#   {'id-produto': 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'nome-do-produto': 'Outro Produto', 'custo-do-produto': '10,50'}
# ]"""