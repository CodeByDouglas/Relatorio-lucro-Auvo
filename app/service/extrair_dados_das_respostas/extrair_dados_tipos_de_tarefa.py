def extrair_tipos_de_tarefa(api_response):
    """
    Recebe o JSON do endpoint de tipos de tarefa e devolve apenas uma lista de dicts:

    [
      {
        "id-tipo-de-tarefa": "...",
        "nome-do-tipo-de-tarefa": "...",
      },
      ...
    ]

    - Mantém somente os campos essenciais.
    - Remove espaços extras no nome.
    """
    tipos = api_response["result"]["entityList"]
    lista = [
        {
            "id-tipo-de-tarefa": t.get("id"),
            "nome-do-tipo-de-tarefa": t.get("description", "").strip()
        }
        for t in tipos
    ]
    return lista

"""resposta_api = {
    "result": {
        "entityList": [
            {"id": 12, "description": "Inspeção técnica"},
            {"id": 34, "description": "Manutenção corretiva"}
        ]
    }
}

tipos = extrair_tipos_de_tarefa(resposta_api)
print(tipos)
# Saída:
# [
#   {'id-tipo-de-tarefa': 12, 'nome-do-tipo-de-tarefa': 'Inspeção técnica'},
#   {'id-tipo-de-tarefa': 34, 'nome-do-tipo-de-tarefa': 'Manutenção corretiva'}
# ]"""