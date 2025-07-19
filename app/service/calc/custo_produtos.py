import re

def calcular_custo_produtos(litagen_id_produtos_tarefas, listagem_json_produtos):
    """
    Soma o 'custo-do-produto' dos produtos cujo 'id-produto' aparece em litagen_id_produtos_tarefas.

    Parâmetros:
        litagen_id_produtos_tarefas       : lista de strings com IDs de produto (podem repetir)
        listagem_json_produtos  : lista de dicts, cada um no formato:
                          {
                            'id-produto': '...',
                            'nome-do-produto': '...',
                            'custo-do-produto': '6,00'  # pode conter formato brasileiro
                          }

    Retorna:
        float -> soma total dos custos correspondentes às ocorrências em litagen_id_produtos_tarefas.

    Regras:
      - Cada ocorrência em litagen_id_produtos_tarefas conta, mesmo que o ID repita.
      - Se um ID de litagen_id_produtos_tarefas não existir em listagem_json_produtos, ele é ignorado.
      - Custos com vírgula decimal ou separadores de milhar são normalizados.
    """
    if not isinstance(litagen_id_produtos_tarefas, list):
        raise ValueError("lista_ids deve ser uma lista.")
    if not isinstance(listagem_json_produtos, list):
        raise ValueError("listagem_json_produtos deve ser uma lista.")

    # Construir mapa id -> custo (float)
    mapa_custos = {}
    for prod in listagem_json_produtos:
        pid = prod.get('id-produto')
        custo_str = (prod.get('custo-do-produto') or "0").strip()
        # Remove pontos (milhar) e troca vírgula por ponto
        custo_norm = re.sub(r'\.', '', custo_str).replace(',', '.')
        try:
            mapa_custos[pid] = float(custo_norm)
        except (ValueError, TypeError):
            mapa_custos[pid] = 0.0

    custo_dos_produtos = 0.0
    for pid in litagen_id_produtos_tarefas:
        # soma para cada ocorrência
        if pid in mapa_custos:
            custo_dos_produtos += mapa_custos[pid]

    return custo_dos_produtos
