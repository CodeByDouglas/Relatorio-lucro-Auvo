import json

def mesclar_extracoes(lista_extracoes):
    """
    Mescla múltiplos objetos no formato 'dados_extraitos' em um único.
    """
    resultado = {
        "dados_extraitos": [
            {
                "estrutura-tarefas": {},
                "produtoID": [],
                "servicoID": [],
                "faturamento-produtos": 0.0,
                "faturamento-servicos": 0.0
            }
        ]
    }
    out = resultado["dados_extraitos"][0]
    contador = 1

    for extracao in lista_extracoes:
        bloco = extracao["dados_extraitos"][0]

        # 1) Reindexar e adicionar tarefas
        for _, tarefa in bloco["estrutura-tarefas"].items():
            nova_chave = f"{contador:02d}"
            out["estrutura-tarefas"][nova_chave] = tarefa
            contador += 1

        # 2) Concatenar IDs
        out["produtoID"].extend(bloco.get("produtoID", []))
        out["servicoID"].extend(bloco.get("servicoID", []))

        # 3) Somar faturamentos
        out["faturamento-produtos"] += bloco.get("faturamento-produtos", 0.0)
        out["faturamento-servicos"] += bloco.get("faturamento-servicos", 0.0)

    return resultado

