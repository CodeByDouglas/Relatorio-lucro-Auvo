import json

def extrair_lista_dados_tarefas(api_responses, filtro_listagem_id_produtos, filtro_listagem_id_servico):
    """
    Consolida múltiplas respostas do endpoint de tarefas em um único JSON.

    Parâmetros:
        api_responses      : lista de objetos (dict) no formato retornado pela API
                              cada item deve possuir ["result"]["entityList"].
        filtro_listagem_id_produtos   : lista NÃO vazia de IDs de produto a considerar.
        filtro_listagem_id_servico   : lista NÃO vazia de IDs de serviço a considerar.

    Requerimentos:
        - filtro_listagem_id_produtos e filtro_listagem_id_servico obrigatórios e não vazios.
        - Ignora (pula) respostas onde:
            * não exista a chave ["result"]["entityList"], ou
            * a lista de tarefas esteja vazia.
        
    
    Retorno:
        {
          "dados_extraitos": [
            {
              "estrutura-tarefas": {
                "01": {...},
                "02": {...},
                ...
              },
              "produtoID": [...],
              "servicoID": [...],
              "faturamento-produtos": <float>,
              "faturamento-servicos": <float>
            }
          ]
        }
    """

    if not isinstance(api_responses, (list, tuple)) or len(api_responses) == 0:
        raise ValueError("Parâmetro 'api_responses' deve ser uma lista não vazia de respostas.")
    if not filtro_listagem_id_produtos:
        raise ValueError("Parâmetro 'filtro_listagem_id_produtos' é obrigatório e não pode ser vazio.")
    if not filtro_listagem_id_servico:
        raise ValueError("Parâmetro 'filtro_listagem_id_servico' é obrigatório e não pode ser vazio.")

    prod_filter = set(filtro_listagem_id_produtos)
    serv_filter = set(filtro_listagem_id_servico)

    estrutura_tarefas = []
    produto_ids_acumulados = []
    servico_ids_acumulados = []
    fatur_total_prod = 0.0
    fatur_total_serv = 0.0

    for resposta in api_responses:
        try:
            tarefas = resposta["result"]["entityList"]
        except (TypeError, KeyError):
            continue
        if not tarefas:
            continue

        for tarefa in tarefas:
            bloco = {
                "id-da-tarefa":      tarefa.get("taskID"),
                "nome-do-cliente":   tarefa.get("customerDescription"),
                "data-da-tarefa":    tarefa.get("taskDate"),
                "tipo-da-tarefa":    tarefa.get("taskType"),
                "id-do-colaborador": tarefa.get("idUserTo"),
            }

            produtos = []
            fatur_prod_local = 0.0
            for p in tarefa.get("products", []):
                pid = p.get("productId")
                if pid in prod_filter:
                    qtd = int(p.get("quantity", 1))
                    produtos.extend([pid] * qtd)
                    fatur_prod_local += p.get("totalValue", 0.0)

            servicos = []
            fatur_serv_local = 0.0
            for s in tarefa.get("services", []):
                sid = s.get("id")
                if sid in serv_filter:
                    qtd = int(s.get("quantity", 1))
                    servicos.extend([sid] * qtd)
                    fatur_serv_local += s.get("totalValue", 0.0)

            bloco["produtos"] = produtos
            bloco["serviços"] = servicos
            bloco["faturamento-produtos"] = fatur_prod_local
            bloco["faturamento-servicos"] = fatur_serv_local

            estrutura_tarefas.append(bloco)

            produto_ids_acumulados.extend(produtos)
            servico_ids_acumulados.extend(servicos)
            fatur_total_prod += fatur_prod_local
            fatur_total_serv += fatur_serv_local

    return {
        "dados_extraidos": [
            {
                "tarefas": estrutura_tarefas,
                "produtoID": produto_ids_acumulados,
                "servicoID": servico_ids_acumulados,
                "faturamento-produtos": fatur_total_prod,
                "faturamento-servicos": fatur_total_serv
            }
        ]
    }

"""input_json = json.loads(input_json_str)
saida = extrair_dados_com_faturamento_por_tarefa(input_json)
print(json.dumps(saida, ensure_ascii=False, indent=2))



{
  "dados_extraitos": [
    {
      "tarefas": [
        {
          "id-da-tarefa": 60966573,
          "nome-do-cliente": "Cliente de Teste",
          "data-da-tarefa": "2025-07-16T13:00:00",
          "tipo-da-tarefa": 182191,
          "id-do-colaborador": 201975,
          "produtos": [
            "9854b8e3-5fa5-11f0-ba85-0a44e9849753",
            "9854b8e3-5fa5-11f0-ba85-0a44e9849753"
          ],
          "serviços": [
            "5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462"
          ],
          "faturamento-produtos": 20.0,
          "faturamento-servicos": 250.0
        },
        {
          "id-da-tarefa": 60966589,
          "nome-do-cliente": "Auvo Tecnologia",
          "data-da-tarefa": "2025-07-16T13:30:00",
          "tipo-da-tarefa": 192651,
          "id-do-colaborador": 198544,
          "produtos": [
            "1f58d4ed-610d-11f0-ba85-0a44e9849753",
            "9854b8e3-5fa5-11f0-ba85-0a44e9849753"
          ],
          "serviços": [],
          "faturamento-produtos": 510.0,
          "faturamento-servicos": 0.0
        },
        {
          "id-da-tarefa": 60966593,
          "nome-do-cliente": "Condomínio Auvo",
          "data-da-tarefa": "2025-07-16T19:05:00",
          "tipo-da-tarefa": 182191,
          "id-do-colaborador": 183873,
          "produtos": [],
          "serviços": [
            "b28117c7-626b-4b53-8462-ff04b4af1a14",
            "b28117c7-626b-4b53-8462-ff04b4af1a14"
          ],
          "faturamento-produtos": 0.0,
          "faturamento-servicos": 1000.0
        }
      ],
      "produtoID": [
        "9854b8e3-5fa5-11f0-ba85-0a44e9849753",
        "9854b8e3-5fa5-11f0-ba85-0a44e9849753",
        "1f58d4ed-610d-11f0-ba85-0a44e9849753",
        "9854b8e3-5fa5-11f0-ba85-0a44e9849753"
      ],
      "servicoID": [
        "5a1b2f65-80b4-11ef-ab1c-0ab8a76e2462",
        "b28117c7-626b-4b53-8462-ff04b4af1a14",
        "b28117c7-626b-4b53-8462-ff04b4af1a14"
      ],
      "faturamento-produtos": 530.0,
      "faturamento-servicos": 1250.0
    }
  ]
}
"""