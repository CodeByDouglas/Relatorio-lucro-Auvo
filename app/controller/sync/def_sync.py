from app.Api.request_produtos import request_produtos_auvo
from app.Api.request_servico import request_servicos_auvo
from app.Api.request_tipo_de_tarefa import request_tipos_de_tarefa_auvo
from app.service.extrair_dados.extrair_json_produtos import extrair_lista_produtos
from app.service.extrair_dados.extrair_json_servicos import extrair_lista_servicos
from app.service.extrair_dados.extrair_json_tipos_de_tarefa import extrair_tipos_de_tarefa
from app.service.paginar_request.request_tarefas_paginadas import request_tarefas_paginadas
from app.service.paginar_request.extrair_lista_json_tarefas import extrair_lista_json_tarefas
from app.service.paginar_request.mesclar_json_fomatado import mesclar_extracoes
from app.service.salvar_no_db.salvar_produtos import salvar_ou_atualizar_produtos
from app.service.salvar_no_db.salvar_servicos import salvar_ou_atualizar_servicos
from app.service.salvar_no_db.salvar_tipos_de_tarefa import salvar_ou_atualizar_tipos_de_tarefa
from app.service.salvar_no_db.salvar_tarefas import salvar_ou_atualizar_tarefas
from app.service.salvar_no_db.salvar_dados_calculados import salvar_ou_atualizar_dados_calculados
from app.service.calc.calcular_custo_produtos import somar_custo_produtos
from app.service.calc.calcular_todos_os_dados import calcular_todos_os_valores


def sync(data_inicial, data_final, id_tipo_de_tarefa, ids_produto_filtrado, ids_servico_filtrado, iduser, token_auth):
    """
    Gera relatório completo com dados de produtos, serviços e tarefas
    
    Args:
        data_inicial (str): Data inicial no formato "YYYY-MM-DD"
        data_final (str): Data final no formato "YYYY-MM-DD"
        id_tipo_de_tarefa (int): ID do tipo de tarefa
        ids_produto_filtrado (list): Lista de IDs de produtos filtrados ou None
        ids_servico_filtrado (list): Lista de IDs de serviços filtrados ou None
        iduser (int): ID do usuário
        token_auth (str): Token de autenticação
        
    Returns:
        dict: JSON com resultados calculados
        
    Raises:
        Exception: Em caso de falha no carregamento de dados
    """
    
    # 1. CARREGAR E SALVAR CATÁLOGOS
    
    # 1.1 – Produtos
    raw_produtos = request_produtos_auvo(token_auth)
    if raw_produtos is None:
        raise Exception("Falha ao carregar produtos")
    
    produtos_formatados = extrair_lista_produtos(raw_produtos)
    salvar_ou_atualizar_produtos(iduser, produtos_formatados)
    
    # 1.2 – Serviços
    raw_servicos = request_servicos_auvo(token_auth)
    if raw_servicos is None:
        raise Exception("Falha ao carregar serviços")
    
    servicos_formatados = extrair_lista_servicos(raw_servicos)
    salvar_ou_atualizar_servicos(iduser, servicos_formatados)
    
    # 1.3 – Tipos de tarefa
    raw_tipos = request_tipos_de_tarefa_auvo(token_auth)
    if raw_tipos is None:
        raise Exception("Falha ao carregar tipos de tarefa")
    
    tipos_formatados = extrair_tipos_de_tarefa(raw_tipos)
    salvar_ou_atualizar_tipos_de_tarefa(iduser, tipos_formatados)
    
    # 2. BUSCAR TAREFAS PAGINADAS
    raw_tarefas = request_tarefas_paginadas(
        data_inicial=data_inicial,
        data_final=data_final,
        id_tipo_de_tarefa=id_tipo_de_tarefa,
        status=3,
        page=1,
        token_autenticacao=token_auth
    )
    
    if raw_tarefas is None or raw_tarefas == "erro":
        raise Exception("Falha ao carregar tarefas")
    
    if not raw_tarefas:  # Lista vazia
        return {}  # Nada a processar
    
    # 2.1 – Definir filtros de IDs
    if ids_produto_filtrado is None or not ids_produto_filtrado:
        # Extrair todos os IDs de produto
        ids_produto_filtrado = []
        for produto in produtos_formatados.get("lista_de_produtos", []):
            ids_produto_filtrado.append(produto["id-produto"])
    
    if ids_servico_filtrado is None or not ids_servico_filtrado:
        # Extrair todos os IDs de serviço
        ids_servico_filtrado = []
        for servico in servicos_formatados.get("lista_de_servicos", []):
            ids_servico_filtrado.append(servico["id-servico"])
    
    # 2.2 – Extrair cada página em JSONs intermediários
    extracoes = extrair_lista_json_tarefas(
        lista_respostas=raw_tarefas,
        allowed_products=ids_produto_filtrado,
        allowed_services=ids_servico_filtrado
    )
    
    # 3. MESCLAR E SALVAR TAREFAS
    resumo = mesclar_extracoes(extracoes)
    tarefas_unificadas = resumo["dados_extraitos"][0]["estrutura-tarefas"]
    salvar_ou_atualizar_tarefas(iduser, tarefas_unificadas)
    
    # 4. CALCULAR CUSTOS E LUCROS
    
    # 4.1 – Somar custo dos produtos filtrados
    custo_total = somar_custo_produtos(
        ids_produto_filtrado,
        produtos_formatados
    )
    
    # 4.2 – Obter faturamentos consolidados
    fatur_produto = resumo["dados_extraitos"][0]["faturamento-produtos"]
    fatur_servico = resumo["dados_extraitos"][0]["faturamento-servicos"]
    
    # 4.3 – Calcular todos os valores e porcentagens
    resultados = calcular_todos_os_valores(
        fatur_produto,
        fatur_servico,
        custo_total
    )
    
    # 4.4 – Persistir resultados finais
    salvar_ou_atualizar_dados_calculados(iduser, resultados)
    
    return resultados
