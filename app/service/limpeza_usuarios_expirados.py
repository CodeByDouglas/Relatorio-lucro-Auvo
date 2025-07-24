from app import db
from app.models.user import User
from app.models.produtos import Produtos
from app.models.servicos import Servicos
from app.models.tarefas import Tarefas
from app.models.tipos_de_tarefas import Tipos_de_tarefas
from app.models.dados_calculados import (
    Faturamento_total, 
    Lucro_total, 
    Faturamento_produtos, 
    Faturamento_servicos, 
    Lucro_produtos, 
    Lucro_servicos
)
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def limpar_usuarios_expirados():
    """
    Identifica usuários onde expiracao + 10 minutos < datetime atual
    e remove o usuário e todos os dados relacionados do banco de dados.
    
    Returns:
        dict: Resultado da operação com contadores de usuários removidos
    """
    try:
        logger.info("🧹 Iniciando limpeza de usuários expirados...")
        
        # Calcular o limite de expiração (datetime atual)
        agora = datetime.utcnow()
        
        # Buscar usuários onde expiracao + 10 minutos < datetime atual
        usuarios_expirados = User.query.filter(
            User.expiracao + timedelta(minutes=10) < agora
        ).all()
        
        if not usuarios_expirados:
            logger.info("✅ Nenhum usuário expirado encontrado")
            return {
                "sucesso": True, 
                "usuarios_removidos": 0,
                "mensagem": "Nenhum usuário expirado encontrado"
            }
        
        usuarios_removidos = 0
        erro_ocorrido = False
        
        for usuario in usuarios_expirados:
            try:
                logger.info(f"🗑️ Removendo usuário ID {usuario.id} (expirado em {usuario.expiracao})")
                
                # Remover dados relacionados ao usuário
                # 1. Dados calculados
                Faturamento_total.query.filter_by(user_id=usuario.id).delete()
                Lucro_total.query.filter_by(user_id=usuario.id).delete()
                Faturamento_produtos.query.filter_by(user_id=usuario.id).delete()
                Faturamento_servicos.query.filter_by(user_id=usuario.id).delete()
                Lucro_produtos.query.filter_by(user_id=usuario.id).delete()
                Lucro_servicos.query.filter_by(user_id=usuario.id).delete()
                
                # 2. Tarefas
                Tarefas.query.filter_by(user_id=usuario.id).delete()
                
                # 3. Tipos de tarefas
                Tipos_de_tarefas.query.filter_by(user_id=usuario.id).delete()
                
                # 4. Produtos
                Produtos.query.filter_by(user_id=usuario.id).delete()
                
                # 5. Serviços
                Servicos.query.filter_by(user_id=usuario.id).delete()
                
                # 6. Por último, remover o usuário
                db.session.delete(usuario)
                
                # Confirmar as alterações para este usuário
                db.session.commit()
                usuarios_removidos += 1
                logger.info(f"✅ Usuário ID {usuario.id} e todos os dados relacionados removidos com sucesso")
                
            except Exception as e:
                # Rollback em caso de erro com usuário específico
                db.session.rollback()
                logger.error(f"❌ Erro ao remover usuário ID {usuario.id}: {e}")
                erro_ocorrido = True
                continue
        
        if erro_ocorrido:
            logger.warning(f"⚠️ Limpeza concluída com erros. {usuarios_removidos} usuários removidos")
            return {
                "sucesso": False,
                "usuarios_removidos": usuarios_removidos,
                "mensagem": f"Limpeza concluída com erros. {usuarios_removidos} usuários removidos"
            }
        else:
            logger.info(f"✅ Limpeza concluída com sucesso. {usuarios_removidos} usuários expirados removidos")
            return {
                "sucesso": True,
                "usuarios_removidos": usuarios_removidos,
                "mensagem": f"Limpeza concluída com sucesso. {usuarios_removidos} usuários expirados removidos"
            }
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Erro crítico durante limpeza de usuários expirados: {e}")
        return {
            "sucesso": False,
            "usuarios_removidos": 0,
            "mensagem": f"Erro crítico durante limpeza: {str(e)}"
        }

def executar_limpeza_agendada():
    """
    Função wrapper para ser chamada pelo scheduler.
    Executa a limpeza e registra os logs adequados.
    """
    logger.info("🕐 Executando limpeza agendada de usuários expirados...")
    resultado = limpar_usuarios_expirados()
    
    if resultado["sucesso"]:
        logger.info(f"📊 {resultado['mensagem']}")
    else:
        logger.error(f"📊 {resultado['mensagem']}")
    
    return resultado