from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Configurações para desenvolvimento
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Iniciando servidor Flask...")
    print(f"📍 Servidor rodando em: http://localhost:{port}")
    print(f"🔧 Modo debug: {debug_mode}")

    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)