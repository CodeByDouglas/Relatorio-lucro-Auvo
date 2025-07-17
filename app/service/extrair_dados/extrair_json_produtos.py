import json

def extrair_lista_produtos(api_response):
    """
    Recebe o JSON da resposta do endpoint e retorna:
    {
      "lista_de_produtos": [
        { "id-produto": "...", "nome-do-produto": "..." },
        ...
      ]
    }
    """
    produtos = api_response["result"]["entityList"]
    
    lista_simplificada = []
    for item in produtos:
        lista_simplificada.append({
            "id-produto":     item["productId"],
            "nome-do-produto": item["name"]
        })
    
    return { "lista_de_produtos": lista_simplificada }