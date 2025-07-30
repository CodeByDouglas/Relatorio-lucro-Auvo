from app.Api.request_produtos import request_produtos_auvo
from app.Api.request_servicos import request_servicos_auvo
from app.Api.request_tipo_de_tarefa import request_tipos_de_tarefa_auvo
from app. Api.request_tarefas import request_tarefas_completa
from app.Api.request_colaboradores import request_colaboradores_auvo
from app.service.extrair_dados_das_respostas.extrair_dados_produto import extrair_lista_produtos
from app.service.extrair_dados_das_respostas.extrair_dados_servicos import extrair_lista_servicos
from app.service.extrair_dados_das_respostas.extrair_dados_tipos_de_tarefa import extrair_tipos_de_tarefa
from app.service.extrair_dados_das_respostas.extrair_dados_tarefas import extrair_lista_dados_tarefas
from app.service.extrair_dados_das_respostas.extrair_dados_colaboradores import extrair_lista_colaboradores
from app.service.salvar_dados_no_banco.salvar_produtos import salvar_ou_atualizar_produtos
from app.service.salvar_dados_no_banco.salvar_servicos import salvar_ou_atualizar_servicos
from app.service.salvar_dados_no_banco.salvar_tipos_de_tarefa import salvar_ou_atualizar_tipos_de_tarefa
from app.service.salvar_dados_no_banco.salvar_tarefas import salvar_ou_atualizar_tarefas
from app.service.salvar_dados_no_banco.salvar_dados_calculados import salvar_ou_atualizar_dados_calculados
from app.service.salvar_dados_no_banco.salvar_colaboradores import salvar_ou_atualizar_colaboradores
from app.service.calc.custo_produtos import calcular_custo_produtos
from app.service.calc.custo_servicos import calcular_custo_servicos
from app.service.calc.calcular_todos_os_dados import calcular_todos_os_valores
from app.service.calc.calcular_todos_os_dados_tarefa_individual import calcular_todos_os_dados_tarefa_individual

def sync(user_id, accessToken, id_produto, id_servico, id_tipo_de_tarefa, start_date, end_date, status, id_colaborador):
    
    # Chama a Api de produtos e atualiza o banco.
    request_produtos = request_produtos_auvo(accessToken)
    if request_produtos is None:
        return False, "API de produtos falhou"
    else:
        produtos = extrair_lista_produtos(request_produtos)
        salvar_ou_atualizar_produtos(user_id, produtos)
    
    # Chama a Api de serviços e atualiza o banco.
    request_servicos = request_servicos_auvo(accessToken)
    if request_servicos is None:
        return False, "API de servicos falhou"
    else:
        servicos = extrair_lista_servicos(request_servicos)
        salvar_ou_atualizar_servicos(user_id, servicos)    
    
    # Chama a Api de tipos de tarefa e atualiza o banco.
    request_tipos_de_tarefa = request_tipos_de_tarefa_auvo(accessToken)
    if request_tipos_de_tarefa is None:
        return False, "API de tipos de tarefa falhou"
    else:
        tipos_de_tarefa = extrair_tipos_de_tarefa(request_tipos_de_tarefa)
        salvar_ou_atualizar_tipos_de_tarefa(user_id, tipos_de_tarefa)
    
    # Chama a Api de colaboradores e atualiza o banco.
    request_colaboradores = request_colaboradores_auvo(accessToken)
    if request_colaboradores is None:
        return False, "API de colaboradores falhou"
    else:
        colaboradores = extrair_lista_colaboradores(request_colaboradores)
        salvar_ou_atualizar_colaboradores(user_id, colaboradores)
    
    #Pega a listagem de dos Id de produtos que tem armazenado para só contar produtos que esteja ativos no sistema. 
    filtro_listagem_id_produtos = [produto['id-produto'] for produto in produtos]
    
    #Pega a listagem de dos Id de serviço que tem armazenado para só contar serviços que esteja ativos no sistema. 
    filtro_listagem_id_servicos = [servico['id-servico'] for servico in servicos]

    #Verifica se está tem algum produto sento filtrado e atualiza os ids de filtro.
    if not(id_produto is None):
        if id_produto in filtro_listagem_id_produtos: 
            filtro_listagem_id_produtos = [id_produto]
        else:
            return False, "O Produto filtrado foi excluido do sistema"
    
    #Verifica se está tem algum serviço sento filtrado e atualiza os ids de filtro.
    if not(id_servico is None):
        if id_servico in filtro_listagem_id_servicos: 
            filtro_listagem_id_servicos = [id_servico]
        else:
            return False, "O Serviço filtrado foi excluido do sistema"
    
    #Faz chama a API que busca as tarefas com os filtros aplicados.
    request_tarefas = request_tarefas_completa(accessToken, start_date, end_date, id_tipo_de_tarefa, status, id_colaborador)

    #Verifica se as tarefas foram encontradas.
    if request_tarefas == []:
        return False, "Falha ao buscar tarefas"
    else:
        #Chama a função que faz a extração dos dados importantes da resposta do endpoint de tarefas. 
        tarefas_e_dados = extrair_lista_dados_tarefas(request_tarefas, filtro_listagem_id_produtos, filtro_listagem_id_servicos)
        
        #Separa as tarefas obtidas do restntante do Json.
        tarefas = tarefas_e_dados["dados_extraidos"][0]["tarefas"]
        #Calcula os dados de cada tarefa individual.
        tarefas =  calcular_todos_os_dados_tarefa_individual(tarefas, produtos, colaboradores)
        #Salva as tarefas no banco de dados.
        salvar_ou_atualizar_tarefas(user_id, tarefas)

        #Obtem a lista de produtos utilizados no calculo.
        litagen_id_produtos_tarefas = tarefas_e_dados["dados_extraidos"][0]["produtoID"]

        #Obtem do Json formatado as informações calculadas de faturamento. 
        faturamento_produtos = tarefas_e_dados["dados_extraidos"][0]["faturamento-produtos"]

        faturamento_servicos = tarefas_e_dados["dados_extraidos"][0]["faturamento-servicos"]

        #Passa a listagem de ids utilizados do calculo e lista dos ids de produto com seus valores de custo obtendo o custo total dos produtos. 
        custo_dos_produtos = calcular_custo_produtos(litagen_id_produtos_tarefas, produtos)

        #Passa a listagem de ids utilizados do calculo e lista dos ids de serviço com seus valores de custo obtendo o custo total dos serviços. 
        custo_dos_servicos = calcular_custo_servicos(tarefas, colaboradores, filtro_listagem_id_servicos)

        #Chama a função que faz o calculo de todos os dados necessarios e salva eles no banco de dados.
        dados_calculados = calcular_todos_os_valores(faturamento_produtos, faturamento_servicos, custo_dos_produtos, custo_dos_servicos)
        salvar_ou_atualizar_dados_calculados(user_id, dados_calculados)

        return True, "Sincronização realizada com sucesso"


        









        