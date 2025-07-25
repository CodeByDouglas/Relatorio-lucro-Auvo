document.addEventListener('DOMContentLoaded', function() {
    const loading = document.getElementById('loading');

    function showLoading() {
        loading.classList.remove('loading-hidden');
    }

    function hideLoading() {
        loading.classList.add('loading-hidden');
    }

    function criarTooltip() {
        let tooltip = document.getElementById('chart-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'chart-tooltip';
            tooltip.className = 'chart-tooltip';
            tooltip.style.display = 'none';
            document.body.appendChild(tooltip);
        }
        return tooltip;
    }

    function mostrarTooltip(texto, evt) {
        const tooltip = criarTooltip();
        tooltip.textContent = texto;
        tooltip.style.display = 'block';
        // Posição do mouse
        const padding = 12;
        let x = evt.clientX + padding;
        let y = evt.clientY + padding;
        // Ajuste para não sair da tela
        if (x + tooltip.offsetWidth > window.innerWidth) {
            x = window.innerWidth - tooltip.offsetWidth - padding;
        }
        if (y + tooltip.offsetHeight > window.innerHeight) {
            y = window.innerHeight - tooltip.offsetHeight - padding;
        }
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
    }
    function esconderTooltip() {
        const tooltip = criarTooltip();
        tooltip.style.display = 'none';
    }

    function desenharGraficoComTooltip(id, porcentagem, corPrincipal, corSecundaria, tipo) {
        // tipo: 'faturamento-servico', 'lucro-servico'
        let svg = `<svg viewBox='0 0 100 100' style='cursor:pointer;'>
            <circle class='grafico-bg' cx='50' cy='50' r='45' fill='none' stroke='${corSecundaria}' stroke-width='10'/>
            <circle class='grafico-fg' cx='50' cy='50' r='45' fill='none' stroke='${corPrincipal}' stroke-width='10' stroke-dasharray='${porcentagem * 2.83} ${(100 - porcentagem) * 2.83}' stroke-dashoffset='0' style='transition: stroke-dasharray 0.6s;' transform='rotate(-90 50 50)'/>
        </svg>`;
        document.getElementById(id).innerHTML = svg + document.getElementById(id).innerHTML.replace(/<svg[\s\S]*<\/svg>/, '');
        const container = document.getElementById(id);
        const svgEl = container.querySelector('svg');
        const bg = container.querySelector('.grafico-bg');
        const fg = container.querySelector('.grafico-fg');
        // Tooltips por tipo
        let tooltipFg = '', tooltipBg = '';
        switch(tipo) {
            case 'faturamento-servico':
                tooltipFg = 'Faturamento serviço';
                break;
            case 'lucro-servico':
                tooltipFg = 'Lucro serviço';
                tooltipBg = 'Faturamento serviço';
                break;
        }
        if (fg) {
            fg.addEventListener('mousemove', (e) => mostrarTooltip(tooltipFg, e));
            fg.addEventListener('mouseleave', esconderTooltip);
        }
        if (bg && tooltipBg) {
            bg.addEventListener('mousemove', (e) => mostrarTooltip(tooltipBg, e));
            bg.addEventListener('mouseleave', esconderTooltip);
        }
        if (svgEl) {
            svgEl.addEventListener('mouseleave', esconderTooltip);
        }
    }

    function desenharGraficoComTooltipAnimado(id, porcentagemFinal, corPrincipal, corSecundaria, tipo) {
        let duracao = 900; // ms
        let fps = 60;
        let steps = Math.round((duracao / 1000) * fps);
        let passo = porcentagemFinal / steps;
        let porcentagemAtual = 0;
        let frame = 0;
        // Descobrir o id do span da porcentagem
        let idPercent = id.replace('grafico', 'percent');
        function desenhar(p) {
            let svg = `<svg viewBox='0 0 100 100' style='cursor:pointer;'>
                <circle class='grafico-bg' cx='50' cy='50' r='45' fill='none' stroke='${corSecundaria}' stroke-width='10'/>
                <circle class='grafico-fg' cx='50' cy='50' r='45' fill='none' stroke='${corPrincipal}' stroke-width='10' stroke-dasharray='${p * 2.83} ${(100 - p) * 2.83}' stroke-dashoffset='0' style='transition: none;' transform='rotate(-90 50 50)'/>
            </svg>`;
            // Reinserir o span da porcentagem junto com o SVG
            document.getElementById(id).innerHTML = svg + `<span class='chart-percent' id='${idPercent}'>${Math.round(p)}%</span>`;
            const container = document.getElementById(id);
            const svgEl = container.querySelector('svg');
            const bg = container.querySelector('.grafico-bg');
            const fg = container.querySelector('.grafico-fg');
            // Tooltips por tipo
            let tooltipFg = '', tooltipBg = '';
            switch(tipo) {
                case 'faturamento-servico': tooltipFg = 'Faturamento serviço'; break;
                case 'lucro-servico': tooltipFg = 'Lucro serviço'; tooltipBg = 'Faturamento serviço'; break;
            }
            if (fg) {
                fg.addEventListener('mousemove', (e) => mostrarTooltip(tooltipFg, e));
                fg.addEventListener('mouseleave', esconderTooltip);
            }
            if (bg && tooltipBg) {
                bg.addEventListener('mousemove', (e) => mostrarTooltip(tooltipBg, e));
                bg.addEventListener('mouseleave', esconderTooltip);
            }
            if (svgEl) {
                svgEl.addEventListener('mouseleave', esconderTooltip);
            }
        }
        function animar() {
            if (frame < steps) {
                desenhar(porcentagemAtual);
                porcentagemAtual += passo;
                frame++;
                requestAnimationFrame(animar);
            } else {
                desenhar(porcentagemFinal);
            }
        }
        animar();
    }

    function definirDatasPadrao() {
        const hoje = new Date();
        const ontem = new Date(hoje);
        ontem.setDate(hoje.getDate() - 1);
        const formatarData = (data) => {
            const ano = data.getFullYear();
            const mes = String(data.getMonth() + 1).padStart(2, '0');
            const dia = String(data.getDate()).padStart(2, '0');
            return `${ano}-${mes}-${dia}`;
        };
        document.getElementById('data-inicial').value = formatarData(ontem);
        document.getElementById('data-final').value = formatarData(hoje);
    }

    async function carregarFiltros() {
        const apiKey = localStorage.getItem('api_key') || '';
        try {
            const response = await fetch(`/filtro/carregar_filtros_servicos?api_key=${apiKey}`);
            if (response.ok) {
                const dados = await response.json();
                // Carregar serviços
                const selectServico = document.getElementById('servico');
                if (selectServico) {
                    const valorAtualServico = selectServico.value;
                    selectServico.innerHTML = '<option value="">Todos</option>';
                    dados.servicos.forEach(servico => {
                        const opt = document.createElement('option');
                        opt.value = servico["id-servico"];
                        opt.textContent = servico["nome-do-servico"];
                        selectServico.appendChild(opt);
                    });
                    if (valorAtualServico) {
                        selectServico.value = valorAtualServico;
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
            const response = await fetch(`/dados/dashboard_servicos?api_key=${apiKey}`);
            if (response.ok) {
                const data = await response.json();
                // Inicializar os números das porcentagens com 0%
                document.getElementById('percent-faturamento-servico').textContent = '0%';
                document.getElementById('percent-lucro-servico').textContent = '0%';
                // Faturamento Serviço
                document.getElementById('valor-faturamento-servico').textContent = `R$ ${Number(data.faturamento_servicos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                desenharGraficoComTooltipAnimado('grafico-faturamento-servico', data.faturamento_servicos.porcentagem_faturamento_total, '#7024c4', '#eaeaea', 'faturamento-servico');
                // Lucro Serviço
                document.getElementById('valor-lucro-servico').textContent = `R$ ${Number(data.lucro_servicos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                desenharGraficoComTooltipAnimado('grafico-lucro-servico', data.lucro_servicos.porcentagem_lucro_total, '#16b14b', '#eaeaea', 'lucro-servico');
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
    document.getElementById('modal-detalhes').addEventListener('click', function(e) {
        if (e.target === this) {
            fecharModal();
        }
    });

    async function carregarDetalhes() {
        showLoading();
        try {
            const apiKey = localStorage.getItem('api_key') || '';
            const response = await fetch(`/dados/detalhes_servicos?api_key=${apiKey}`);
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
        const servico = document.getElementById('servico').value;
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
                    id_produto: null,
                    id_servico: servico || null,
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

    // Botão GERAL: faz sync e redireciona igual dashboard_produtos
    const btnGeral = document.querySelector('.nav-btns .nav-btn');
    if (btnGeral) {
        btnGeral.addEventListener('click', async function(e) {
            e.preventDefault();
            showLoading();
            const apiKey = localStorage.getItem('api_key') || '';
            // Datas: ontem e hoje
            const hoje = new Date();
            const ontem = new Date(hoje);
            ontem.setDate(hoje.getDate() - 1);
            function formatarData(data) {
                const ano = data.getFullYear();
                const mes = String(data.getMonth() + 1).padStart(2, '0');
                const dia = String(data.getDate()).padStart(2, '0');
                return `${ano}-${mes}-${dia}`;
            }
            const start_date = formatarData(ontem);
            const end_date = formatarData(hoje);
            try {
                const response = await fetch('/sync', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        api_key: apiKey,
                        id_produto: null,
                        id_servico: null,
                        id_tipo_de_tarefa: null,
                        start_date,
                        end_date
                    })
                });
                hideLoading();
                if (response.status === 200) {
                    window.location.href = '/dashboard_geral';
                } else if (response.status === 401) {
                    alert('A autenticação expirou. Faça login novamente.');
                } else if (response.status === 400) {
                    alert('Erro ao sincronizar tarefas.');
                } else {
                    alert('Erro inesperado ao sincronizar.');
                }
            } catch (err) {
                hideLoading();
                alert('Erro de conexão ao sincronizar.');
            }
        });
    }
    // Botão PRODUTO: redireciona
    const btnProduto = document.querySelectorAll('.nav-btns .nav-btn')[1];
    if (btnProduto) {
        btnProduto.addEventListener('click', function() {
            window.location.href = '/dashboard_produtos';
        });
    }
    // Botão SERVIÇO: não faz nada (ativo)

    fecharModal();
    Promise.all([
        carregarFiltros(),
        carregarDashboard()
    ]).then(() => {
        definirDatasPadrao();
    });
});
