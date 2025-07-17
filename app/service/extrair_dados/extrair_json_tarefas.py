import json

def extrair_json_tarefas(
    api_response,
    allowed_products=None,
    allowed_services=None
):
    tarefas = api_response["result"]["entityList"]
    estrutura = {}

    prod_filter = set(allowed_products) if allowed_products else None
    serv_filter = set(allowed_services) if allowed_services else None

    for i, tarefa in enumerate(tarefas, start=1):
        key = f"{i:02d}"
        bloco = {
            "id-da-tarefa":      tarefa["taskID"],
            "nome-do-cliente":   tarefa["customerDescription"],
            "data-da-tarefa":    tarefa["taskDate"],
            "tipo-da-tarefa":    tarefa["taskType"],
            "id-do-colaborador": tarefa["idUserTo"],
        }

        produtos = []
        fatur_prod = 0.0
        for p in tarefa.get("products", []):
            pid = p["productId"]
            if prod_filter is None or pid in prod_filter:
                qtd = int(p["quantity"])
                produtos += [pid] * qtd
                fatur_prod += p.get("totalValue", 0.0)

        servicos = []
        fatur_serv = 0.0
        for s in tarefa.get("services", []):
            sid = s["id"]
            if serv_filter is None or sid in serv_filter:
                qtd = int(s.get("quantity", 1))
                servicos += [sid] * qtd
                fatur_serv += s.get("totalValue", 0.0)

        bloco["produtos"] = produtos
        bloco["serviços"] = servicos
        bloco["faturamento-produtos"] = fatur_prod
        bloco["faturamento-servicos"] = fatur_serv
        estrutura[key] = bloco

    todos_produtos = [pid for b in estrutura.values() for pid in b["produtos"]]
    todos_servicos = [sid for b in estrutura.values() for sid in b["serviços"]]
    fatur_total_prod = sum(
        p["totalValue"]
        for t in tarefas
        for p in t.get("products", [])
        if prod_filter is None or p["productId"] in prod_filter
    )
    fatur_total_serv = sum(
        s["totalValue"]
        for t in tarefas
        for s in t.get("services", [])
        if serv_filter is None or s["id"] in serv_filter
    )

    return {
        "dados_extraitos": [
            {
                "estrutura-tarefas": estrutura,
                "produtoID": todos_produtos,
                "servicoID": todos_servicos,
                "faturamento-produtos": fatur_total_prod,
                "faturamento-servicos": fatur_total_serv
            }
        ]
    }