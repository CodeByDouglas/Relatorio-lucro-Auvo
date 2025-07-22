from app.Api.request_produtos import request_produtos_auvo
from app.Api.request_servico import request_servicos_auvo
from app.Api.request_tipo_de_tarefa import request_tipos_de_tarefa_auvo
from app. Api.request_tarefas import request_tarefas_completa
from app.service.extrair_dados_das_respostas.extrair_dados_produto import extrair_lista_produtos
from app.service.extrair_dados_das_respostas.extrair_dados_servicos import extrair_lista_servicos
from app.service.extrair_dados_das_respostas.extrair_dados_tipos_de_tarefa import extrair_tipos_de_tarefa
from app.service.extrair_dados_das_respostas.extrair_dados_tarefas import extrair_lista_dados_tarefas
from app.service.salvar_dados_no_banco.salvar_produtos import salvar_ou_atualizar_produtos
from app.service.salvar_dados_no_banco.salvar_servicos import salvar_ou_atualizar_servicos
from app.service.salvar_dados_no_banco.salvar_tipos_de_tarefa import salvar_ou_atualizar_tipos_de_tarefa
from app.service.salvar_dados_no_banco.salvar_tarefas import salvar_ou_atualizar_tarefas
from app.service.salvar_dados_no_banco.salvar_dados_calculados import salvar_ou_atualizar_dados_calculados
from app.service.calc.custo_produtos import calcular_custo_produtos
from app.service.calc.calcular_todos_os_dados import calcular_todos_os_valores

def sync(user_id, accessToken, id_produto, id_servico, id_tipo_de_tarefa, start_date, end_date):
    
    # Chamar API de produtos
    request_produtos = request_produtos_auvo(accessToken)
    if request_produtos is None:
        return False, "API de produtos falhou"
    else:
        produtos = extrair_lista_produtos(request_produtos)
        salvar_ou_atualizar_produtos(user_id, produtos)
    
    # Chamar API de serviços
    request_servicos = request_servicos_auvo(accessToken)
    if request_servicos is None:
        return False, "API de servicos falhou"
    else:
        servicos = extrair_lista_servicos(request_servicos)
        salvar_ou_atualizar_servicos(user_id, servicos)    
    
    # Chamar API de tipos de tarefa
    request_tipos_de_tarefa = request_tipos_de_tarefa_auvo(accessToken)
    if request_tipos_de_tarefa is None:
        return False, "API de tipos de tarefa falhou"
    else:
        tipos_de_tarefa = extrair_tipos_de_tarefa(request_tipos_de_tarefa)
        salvar_ou_atualizar_tipos_de_tarefa(user_id, tipos_de_tarefa)
    
    
    filtro_listagem_id_produtos = [produto['id-produto'] for produto in produtos]
    
    
    filtro_listagem_id_servicos = [servico['id-servico'] for servico in servicos]
    
    if not(id_produto is None):
        if id_produto in filtro_listagem_id_produtos: 
            filtro_listagem_id_produtos = [id_produto]
        else:
            return False, "O Produto filtrado foi excluido do sistema"
    
    if not(id_servico is None):
        if id_servico in filtro_listagem_id_servicos: 
            filtro_listagem_id_servicos = [id_servico]
        else:
            return False, "O Serviço filtrado foi excluido do sistema"
        
    request_tarefas = request_tarefas_completa(accessToken, start_date, end_date, id_tipo_de_tarefa)
    if request_tarefas is None:
        return False, "Falha ao buscar tarefas"
    else:
        tarefas_e_dados = extrair_lista_dados_tarefas(request_tarefas, filtro_listagem_id_produtos, filtro_listagem_id_servicos)
        tarefas = tarefas_e_dados["dados_extraitos"][0]["tarefas"]
        salvar_ou_atualizar_tarefas(user_id, tarefas)

        litagen_id_produtos_tarefas = tarefas_e_dados["dados_extraitos"][0]["produtoID"]

        faturamento_produtos = tarefas_e_dados["dados_extraitos"][0]["faturamento-produtos"]

        faturamento_servicos = tarefas_e_dados["dados_extraitos"][0]["faturamento-servicos"]

        custo_dos_produtos = calcular_custo_produtos(litagen_id_produtos_tarefas, produtos)

        dados_calculados = calcular_todos_os_valores(faturamento_produtos, faturamento_servicos, custo_dos_produtos)

        salvar_ou_atualizar_dados_calculados(user_id, dados_calculados)

        return True


        









        