document.addEventListener('DOMContentLoaded', function() {
    const loading = document.getElementById('loading');
    
    function showLoading() {
        loading.classList.remove('loading-hidden');
    }
    
    function hideLoading() {
        loading.classList.add('loading-hidden');
    }
    
    function desenharGrafico(id, porcentagem, corPrincipal, corSecundaria) {
        const svg = `<svg viewBox='0 0 100 100'>
            <circle cx='50' cy='50' r='45' fill='none' stroke='${corSecundaria}' stroke-width='10'/>
            <circle cx='50' cy='50' r='45' fill='none' stroke='${corPrincipal}' stroke-width='10' stroke-dasharray='${porcentagem * 2.83} ${(100 - porcentagem) * 2.83}' stroke-dashoffset='0' style='transition: stroke-dasharray 0.6s;' transform='rotate(-90 50 50)'/>
        </svg>`;
        document.getElementById(id).innerHTML = svg + document.getElementById(id).innerHTML.replace(/<svg[\s\S]*<\/svg>/, '');
    }
    
    function definirDatasPadrao() {
        const hoje = new Date();
        const ontem = new Date(hoje);
        ontem.setDate(hoje.getDate() - 1);
        
        // Formatar datas para o formato YYYY-MM-DD (padrão do input date)
        const formatarData = (data) => {
            const ano = data.getFullYear();
            const mes = String(data.getMonth() + 1).padStart(2, '0');
            const dia = String(data.getDate()).padStart(2, '0');
            return `${ano}-${mes}-${dia}`;
        };
        
        // Definir valores padrão
        document.getElementById('data-inicial').value = formatarData(ontem);
        document.getElementById('data-final').value = formatarData(hoje);
    }
    
    async function carregarFiltros() {
        const apiKey = localStorage.getItem('api_key') || '';
        try {
            const response = await fetch(`/filtro/carregar_filtros_produtos?api_key=${apiKey}`);
            if (response.ok) {
                const dados = await response.json();
                
                // Carregar produtos
                const selectProduto = document.getElementById('produto');
                if (selectProduto) {
                    const valorAtualProduto = selectProduto.value;
                    selectProduto.innerHTML = '<option value="">Todos</option>';
                    dados.produtos.forEach(produto => {
                        const opt = document.createElement('option');
                        opt.value = produto["id-produto"];
                        opt.textContent = produto["nome-do-produto"];
                        selectProduto.appendChild(opt);
                    });
                    if (valorAtualProduto) {
                        selectProduto.value = valorAtualProduto;
                    }
                }
                
                // Carregar tipos de tarefa
                const selectTipoTarefa = document.getElementById('tipo-tarefa');
                if (selectTipoTarefa) {
                    const valorAtualTipoTarefa = selectTipoTarefa.value;
                    selectTipoTarefa.innerHTML = '<option value="">Todos</option>';
                    dados.tipos_tarefa.forEach(tipo => {
                        const opt = document.createElement('option');
                        opt.value = tipo["id-tipo-de-tarefa"];
                        opt.textContent = tipo["nome-do-tipo-de-tarefa"];
                        selectTipoTarefa.appendChild(opt);
                    });
                    if (valorAtualTipoTarefa) {
                        selectTipoTarefa.value = valorAtualTipoTarefa;
                    }
                }
            }
        } catch (e) {
            // Pode exibir erro se desejar
        }
    }
    
    async function carregarDashboard() {
        showLoading();
        try {
            const apiKey = localStorage.getItem('api_key') || '';
            const response = await fetch(`/dados/dashboard_produtos?api_key=${apiKey}`);
            if (response.ok) {
                const data = await response.json();
                
                // Faturamento Produto
                const percentFaturamentoProduto = Math.round(data.faturamento_produtos.porcentagem_faturamento_total);
                document.getElementById('valor-faturamento-produto').textContent = `R$ ${Number(data.faturamento_produtos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-faturamento-produto').textContent = `${percentFaturamentoProduto}%`;
                desenharGrafico('grafico-faturamento-produto', data.faturamento_produtos.porcentagem_faturamento_total, '#7024c4', '#eaeaea');
                
                // Lucro Produto
                const percentLucroProduto = Math.round(data.lucro_produtos.porcentagem_lucro_total);
                document.getElementById('valor-lucro-produto').textContent = `R$ ${Number(data.lucro_produtos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-lucro-produto').textContent = `${percentLucroProduto}%`;
                desenharGrafico('grafico-lucro-produto', data.lucro_produtos.porcentagem_lucro_total, '#16b14b', '#eaeaea');
            }
        } catch (e) {
            // Pode exibir erro se desejar
        } finally {
            hideLoading();
        }
    }
    
    // Event listeners para o modal de detalhes
    document.getElementById('btn-detalhes').addEventListener('click', carregarDetalhes);
    document.getElementById('btn-fechar-modal').addEventListener('click', fecharModal);
    
    // Fechar modal ao clicar fora dele
    document.getElementById('modal-detalhes').addEventListener('click', function(e) {
        if (e.target === this) {
            fecharModal();
        }
    });
    
    async function carregarDetalhes() {
        showLoading();
        try {
            const apiKey = localStorage.getItem('api_key') || '';
            const response = await fetch(`/dados/detalhes_produtos?api_key=${apiKey}`);
            
            if (response.ok) {
                const tarefas = await response.json();
                preencherTabelaTarefas(tarefas);
                abrirModal();
            } else {
                alert('Erro ao carregar detalhes das tarefas.');
            }
        } catch (error) {
            alert('Erro ao carregar detalhes das tarefas.');
        } finally {
            hideLoading();
        }
    }
    
    function preencherTabelaTarefas(tarefas) {
        const tbody = document.getElementById('tarefas-tbody');
        tbody.innerHTML = '';
        
        tarefas.forEach(tarefa => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${tarefa['id-da-tarefa']}</td>
                <td>${formatarData(tarefa['data-da-tarefa'])}</td>
                <td>${tarefa['nome-do-cliente']}</td>
                <td>R$ ${Number(tarefa['faturamento-total']).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
                <td>R$ ${Number(tarefa['lucro-total']).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
            `;
            tbody.appendChild(row);
        });
    }
    
    function formatarData(dataString) {
        const data = new Date(dataString);
        return data.toLocaleDateString('pt-BR');
    }
    
    function abrirModal() {
        document.getElementById('modal-detalhes').classList.remove('modal-hidden');
    }
    
    function fecharModal() {
        document.getElementById('modal-detalhes').classList.add('modal-hidden');
    }
    
    // Event listener para o formulário de filtros
    document.getElementById('filtros-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Capturar valores dos campos
        const dataInicial = document.getElementById('data-inicial').value;
        const dataFinal = document.getElementById('data-final').value;
        const produto = document.getElementById('produto').value;
        const tipoTarefa = document.getElementById('tipo-tarefa').value;
        
        // Validar datas
        if (new Date(dataFinal) < new Date(dataInicial)) {
            alert('A data inicial não pode ser maior que a data final.');
            return;
        }
        
        const apiKey = localStorage.getItem('api_key') || '';
        showLoading();
        
        try {
            const response = await fetch('/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: apiKey,
                    id_produto: produto || null,
                    id_servico: null,
                    id_tipo_de_tarefa: tipoTarefa || null,
                    start_date: dataInicial,
                    end_date: dataFinal
                })
            });
            
            if (response.status === 401) {
                alert('O acesso do usuário expirou. Você será redirecionado para a tela de login.');
                window.location.href = '/login';
                return;
            }
            
            if (response.status === 400) {
                alert('A sincronização falhou.');
                hideLoading();
                return;
            }
            
            if (response.status === 200) {
                // Recarregar dados do dashboard e filtros
                await Promise.all([
                    carregarFiltros(),
                    carregarDashboard()
                ]);
                alert('Sincronização realizada com sucesso!');
            }
            
        } catch (error) {
            alert('Erro ao realizar sincronização.');
        } finally {
            hideLoading();
        }
    });
    
    // Garantir que o modal comece fechado
    fecharModal();
    
    Promise.all([
        carregarFiltros(),
        carregarDashboard()
    ]).then(() => {
        definirDatasPadrao();
    });
});
