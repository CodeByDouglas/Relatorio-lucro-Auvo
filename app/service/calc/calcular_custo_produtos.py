import re

def somar_custo_produtos(ids, produtos_json):
    """
    Recebe:
      - ids: lista de strings com 'id-produto'
      - produtos_json: dict com chave "lista_de_produtos", valor é lista de dicts contendo:
          - "id-produto"
          - "nome-do-produto"
          - "custo-do-produto" (string, ex: "6,00" ou "12.345,67")
    Retorna a soma dos valores de 'custo-do-produto' correspondentes aos ids na lista.
    """
    # Cria um dicionário de preços: id-produto -> float
    preco_map = {}
    for prod in produtos_json.get("lista_de_produtos", []):
        custo_str = prod.get("custo-do-produto", "0").strip()
        # Remove pontos de milhar e substitui vírgula decimal por ponto
        cleaned = re.sub(r'\.', '', custo_str).replace(',', '.')
        try:
            preco_map[prod["id-produto"]] = float(cleaned)
        except ValueError:
            preco_map[prod["id-produto"]] = 0.0

    # Soma os custos para cada ocorrência no array de ids
    total = 0.0
    for pid in ids:
        total += preco_map.get(pid, 0.0)

    return total