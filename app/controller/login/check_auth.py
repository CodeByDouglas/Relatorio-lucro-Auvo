from app.models.user import User
from app.Api.authe_api_auvo import autenticar_api_auvo
from app import db
from datetime import datetime, timedelta

def check_auth(api_key):
    # Buscar user por api_key
    user = User.query.filter_by(api_key=api_key).first()
    
    if not user:
        return False, "user não logado", None
    
    # Verificar se (expiracao - 5 min) > Horário atual
    limite_expiracao = user.expiracao - timedelta(minutes=5)
    horario_atual = datetime.utcnow()
    
    if limite_expiracao <= horario_atual:
        # Precisa renovar autenticação
        api_token = user.api_token
        resultado = autenticar_api_auvo(api_key, api_token)
        
        if resultado[0] == 200 and resultado[1] == True:
            expiration = resultado[2]
            accessToken = resultado[3]
            
            # Atualizar user
            expiration_datetime = datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S')
            user.expiracao = expiration_datetime
            user.accessToken = accessToken
            db.session.commit()
            
            return True, "Autenticação renovada", accessToken
        else:
            return False, "Não foi póssivel autenticar o user", None
    else:
        # User ainda autenticado
        accessToken = user.accessToken
        return True, "User autenticado", accessToken