import json

def extrair_lista_servicos(api_response):
    """
    Recebe o JSON da resposta do endpoint e retorna:
    {
      "lista_de_servicos": [
        { "id-servico": "...", "nome-do-servico": "..." },
        ...
      ]
    }
    """
    servicos = api_response["result"]["entityList"]
    return {
        "lista_de_servicos": [
            {
                "id-servico": s["id"],
                "nome-do-servico": s["title"]
            }
            for s in servicos
        ]
    }