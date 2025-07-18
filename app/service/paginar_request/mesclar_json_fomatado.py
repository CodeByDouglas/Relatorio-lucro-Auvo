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

# Dados de teste fornecidos
lista_de_jsons = [
    {
      "dados_extraitos": [
        {
          "estrutura-tarefas": {
            "01": {
              "id-da-tarefa": 60966573,
              "nome-do-cliente": "Cliente de Teste",
              "data-da-tarefa": "2025-07-16T13:00:00",
              "tipo-da-tarefa": 182191,
              "id-do-colaborador": 201975,
              "produtos": ["9854b8e3-5fa5-11f0-ba85-0a44e9849753"]*2,
              "serviços": ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462"],
              "faturamento-produtos": 20.0,
              "faturamento-servicos": 250.0
            },
            "02": {
              "id-da-tarefa": 60966589,
              "nome-do-cliente": "Auvo Tecnogia",
              "data-da-tarefa": "2025-07-16T13:30:00",
              "tipo-da-tarefa": 192651,
              "id-do-colaborador": 198544,
              "produtos": ["1f58d4ed-610d-11f0-ba85-0a44e9849753", "9854b8e3-5fa5-11f0-ba85-0a44e9849753"],
              "serviços": [],
              "faturamento-produtos": 510.0,
              "faturamento-servicos": 0.0
            },
            "03": {
              "id-da-tarefa": 60966593,
              "nome-do-cliente": "Condomínio Auvo",
              "data-da-tarefa": "2025-07-16T19:05:00",
              "tipo-da-tarefa": 182191,
              "id-do-colaborador": 183873,
              "produtos": [],
              "serviços": ["b28117c7-626b-4b53-8462-ff04b4af1a14"]*2,
              "faturamento-produtos": 0.0,
              "faturamento-servicos": 1000.0
            }
          },
          "produtoID": ["9854b8e3-5fa5-11f0-ba85-0a44e9849753"]*2 + ["1f58d4ed-610d-11f0-ba85-0a44e9849753", "9854b8e3-5fa5-11f0-ba85-0a44e9849753"],
          "servicoID": ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462", "b28117c7-626b-4b53-8462-ff04b4af1a14", "b28117c7-626b-4b53-8462-ff04b4af1a14"],
          "faturamento-produtos": 530.0,
          "faturamento-servicos": 1250.0
        }
      ]
    },
    {
      "dados_extraitos": [
        {
          "estrutura-tarefas": {
            "01": {
              "id-da-tarefa": 60966573,
              "nome-do-cliente": "Cliente de Teste",
              "data-da-tarefa": "2025-07-16T13:00:00",
              "tipo-da-tarefa": 182191,
              "id-do-colaborador": 201975,
              "produtos": ["9854b8e3-5fa5-11f0-ba85-0a44e9849753"]*2,
              "serviços": ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462"],
              "faturamento-produtos": 20.0,
              "faturamento-servicos": 250.0
            },
            "02": {
              "id-da-tarefa": 60966589,
              "nome-do-cliente": "Auvo Tecnogia",
              "data-da-tarefa": "2025-07-16T13:30:00",
              "tipo-da-tarefa": 192651,
              "id-do-colaborador": 198544,
              "produtos": ["1f58d4ed-610d-11f0-ba85-0a44e9849753", "9854b8e3-5fa5-11f0-ba85-0a44e9849753"],
              "serviços": [],
              "faturamento-produtos": 510.0,
              "faturamento-servicos": 0.0
            },
            "03": {
              "id-da-tarefa": 60966593,
              "nome-do-cliente": "Condomínio Auvo",
              "data-da-tarefa": "2025-07-16T19:05:00",
              "tipo-da-tarefa": 182191,
              "id-do-colaborador": 183873,
              "produtos": [],
              "serviços": ["b28117c7-626b-4b53-8462-ff04b4af1a14"]*2,
              "faturamento-produtos": 0.0,
              "faturamento-servicos": 1000.0
            }
          },
          "produtoID": ["9854b8e3-5fa5-11f0-ba85-0a44e9849753"]*2 + ["1f58d4ed-610d-11f0-ba85-0a44e9849753", "9854b8e3-5fa5-11f0-ba85-0a44e9849753"],
          "servicoID": ["5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462", "b28117c7-626b-4b53-8462-ff04b4af1a14", "b28117c7-626b-4b53-8462-ff04b4af1a14"],
          "faturamento-produtos": 530.0,
          "faturamento-servicos": 1250.0
        }
      ]
    }
]
