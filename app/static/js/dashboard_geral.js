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
    async function carregarDashboard() {
        showLoading();
        try {
            const apiKey = localStorage.getItem('api_key') || '';
            const response = await fetch(`https://6bc486485dab.ngrok-free.app/dados/dashboard_geral?api_key=${apiKey}`);
            if (response.ok) {
                const data = await response.json();
                // Faturamento Total
                const percentFaturamentoTotal = Math.round(data.faturamento_total.porcentagem_total_faturamento);
                document.getElementById('valor-faturamento-total').textContent = `R$ ${Number(data.faturamento_total.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-faturamento-total').textContent = `${percentFaturamentoTotal}%`;
                desenharGrafico('grafico-faturamento-total', 100, '#7024c4', '#eaeaea');
                // Faturamento Produto
                const percentFaturamentoProduto = Math.round(data.faturamento_produtos.porcentagem_faturamento_total);
                document.getElementById('valor-faturamento-produto').textContent = `R$ ${Number(data.faturamento_produtos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-faturamento-produto').textContent = `${percentFaturamentoProduto}%`;
                desenharGrafico('grafico-faturamento-produto', data.faturamento_produtos.porcentagem_faturamento_total, '#7024c4', '#eaeaea');
                // Faturamento Serviço
                const percentFaturamentoServico = Math.round(data.faturamento_servicos.porcentagem_faturamento_total);
                document.getElementById('valor-faturamento-servico').textContent = `R$ ${Number(data.faturamento_servicos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-faturamento-servico').textContent = `${percentFaturamentoServico}%`;
                desenharGrafico('grafico-faturamento-servico', data.faturamento_servicos.porcentagem_faturamento_total, '#7024c4', '#eaeaea');
                // Lucro Total
                const percentLucroTotal = Math.round(data.lucro_total.porcentagem_faturamento_total);
                document.getElementById('valor-lucro-total').textContent = `R$ ${Number(data.lucro_total.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-lucro-total').textContent = `${percentLucroTotal}%`;
                desenharGrafico('grafico-lucro-total', data.lucro_total.porcentagem_faturamento_total, '#16b14b', '#eaeaea');
                // Lucro Produto
                const percentLucroProduto = Math.round(data.lucro_produtos.porcentagem_lucro_total);
                document.getElementById('valor-lucro-produto').textContent = `R$ ${Number(data.lucro_produtos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-lucro-produto').textContent = `${percentLucroProduto}%`;
                desenharGrafico('grafico-lucro-produto', data.lucro_produtos.porcentagem_lucro_total, '#16b14b', '#eaeaea');
                // Lucro Serviço
                const percentLucroServico = Math.round(data.lucro_servicos.porcentagem_lucro_total);
                document.getElementById('valor-lucro-servico').textContent = `R$ ${Number(data.lucro_servicos.valor).toLocaleString('pt-BR', {minimumFractionDigits: 2})}`;
                document.getElementById('percent-lucro-servico').textContent = `${percentLucroServico}%`;
                desenharGrafico('grafico-lucro-servico', data.lucro_servicos.porcentagem_lucro_total, '#16b14b', '#eaeaea');
            }
        } catch (e) {
            // Pode exibir erro se desejar
        } finally {
            hideLoading();
        }
    }
    carregarDashboard();
});
