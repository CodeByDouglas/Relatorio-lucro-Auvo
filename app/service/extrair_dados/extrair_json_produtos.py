import json

def extrair_lista_produtos(api_response):
    """
    Recebe o JSON da resposta do endpoint de produtos e retorna:
    {
      "lista_de_produtos": [
        {
          "id-produto": "...",
          "nome-do-produto": "...",
          "custo-do-produto": "..."
        },
        ...
      ]
    }
    """
    produtos = api_response["result"]["entityList"]
    return {
        "lista_de_produtos": [
            {
                "id-produto":      p["productId"],
                "nome-do-produto": p["name"].strip(),
                "custo-do-produto": p["unitaryCost"]
            }
            for p in produtos
        ]
    }