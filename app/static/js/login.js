document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const appkeyInput = document.getElementById('appkey');
    const tokenInput = document.getElementById('token');
    const loading = document.getElementById('loading');
    const messageContainer = document.getElementById('message-container');

    function showLoading() {
        loading.classList.remove('loading-hidden');
    }
    function hideLoading() {
        loading.classList.add('loading-hidden');
    }
    function showMessage(msg) {
        messageContainer.textContent = msg;
        messageContainer.style.display = 'block';
        setTimeout(() => {
            messageContainer.style.display = 'none';
        }, 3500);
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const appkey = appkeyInput.value.trim();
        const token = tokenInput.value.trim();
        if (!appkey || !token) {
            showMessage('Preencha todos os campos.');
            return;
        }
        showLoading();
        try {
            const response = await fetch(' https://6bc486485dab.ngrok-free.app/logar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ api_key: appkey, api_token: token })
            });
            hideLoading();
            if (response.status === 401) {
                showMessage('Credenciais inválidas');
            } else if (response.status === 500) {
                showMessage('Não foi possível se conectar à API Auvo');
            } else if (response.status === 200) {
                // Salva a api_key no localStorage
                localStorage.setItem('api_key', appkey);
                window.location.href = '/dashboard_geral';
            } else {
                showMessage('Erro inesperado.');
            }
        } catch (err) {
            hideLoading();
            showMessage('Erro de conexão.');
        }
    });
});
