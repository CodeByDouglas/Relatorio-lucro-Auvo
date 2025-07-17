import json

def extrair_tipos_de_tarefa(api_response):
    """
    Recebe o JSON da resposta do endpoint de tipos de tarefa e retorna:
    {
      "lista_de_tipos_de_tarefa": [
        { "id-tipo-de-tarefa": ..., "nome-do-tipo-de-tarefa": ... },
        ...
      ]
    }
    """
    tipos = api_response["result"]["entityList"]
    lista_simplificada = [
        {
            "id-tipo-de-tarefa":      tipo["id"],
            "nome-do-tipo-de-tarefa": tipo["description"]
        }
        for tipo in tipos
    ]
    return {"lista_de_tipos_de_tarefa": lista_simplificada}