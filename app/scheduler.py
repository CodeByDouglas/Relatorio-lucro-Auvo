from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
import logging
import atexit

logger = logging.getLogger(__name__)

scheduler = None

def init_scheduler(app):
    """
    Inicializa o scheduler de tarefas da aplicação
    
    Args:
        app: Instância da aplicação Flask
    """
    global scheduler
    
    if scheduler is not None:
        logger.warning("⚠️ Scheduler já foi inicializado")
        return scheduler
    
    try:
        # Configurações do scheduler
        executors = {
            'default': ThreadPoolExecutor(max_workers=2)
        }
        
        job_defaults = {
            'coalesce': True,  # Evita execução múltipla da mesma tarefa
            'max_instances': 1,  # Máximo 1 instância da tarefa por vez
            'misfire_grace_time': 300  # 5 minutos de tolerância para tarefas atrasadas
        }
        
        # Inicializar scheduler
        scheduler = BackgroundScheduler(
            executors=executors,
            job_defaults=job_defaults,
            timezone='UTC'
        )
        
        logger.info("🚀 Scheduler inicializado com sucesso")
        
        # Configurar tarefas agendadas
        _configurar_tarefas_agendadas(app)
        
        # Iniciar scheduler
        scheduler.start()
        logger.info("▶️ Scheduler iniciado com sucesso")
        
        # Registrar shutdown do scheduler ao finalizar aplicação
        atexit.register(lambda: shutdown_scheduler())
        
        return scheduler
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar scheduler: {e}")
        raise e

def _configurar_tarefas_agendadas(app):
    """
    Configura todas as tarefas agendadas da aplicação
    
    Args:
        app: Instância da aplicação Flask
    """
    global scheduler
    
    try:
        # Tarefa de limpeza de usuários expirados - a cada 5 horas
        from app.service.limpeza_usuarios_expirados import executar_limpeza_agendada
        
        scheduler.add_job(
            func=lambda: _executar_com_contexto_app(app, executar_limpeza_agendada),
            trigger=IntervalTrigger(hours=5),
            id='limpeza_usuarios_expirados',
            name='Limpeza de Usuários Expirados',
            replace_existing=True
        )
        
        logger.info("⏰ Tarefa agendada configurada: Limpeza de usuários expirados (a cada 5 horas)")
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar tarefas agendadas: {e}")
        raise e

def _executar_com_contexto_app(app, funcao):
    """
    Executa uma função dentro do contexto da aplicação Flask
    
    Args:
        app: Instância da aplicação Flask
        funcao: Função a ser executada
    """
    try:
        with app.app_context():
            return funcao()
    except Exception as e:
        logger.error(f"❌ Erro ao executar tarefa agendada: {e}")
        raise e

def adicionar_tarefa(func, trigger, job_id, name, **kwargs):
    """
    Adiciona uma nova tarefa ao scheduler
    
    Args:
        func: Função a ser executada
        trigger: Trigger do APScheduler (IntervalTrigger, CronTrigger, etc.)
        job_id: ID único da tarefa
        name: Nome descritivo da tarefa
        **kwargs: Argumentos adicionais para o job
    """
    global scheduler
    
    if scheduler is None:
        logger.error("❌ Scheduler não foi inicializado")
        return False
    
    try:
        scheduler.add_job(
            func=func,
            trigger=trigger,
            id=job_id,
            name=name,
            replace_existing=True,
            **kwargs
        )
        logger.info(f"✅ Tarefa '{name}' adicionada com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao adicionar tarefa '{name}': {e}")
        return False

def remover_tarefa(job_id):
    """
    Remove uma tarefa do scheduler
    
    Args:
        job_id: ID da tarefa a ser removida
    """
    global scheduler
    
    if scheduler is None:
        logger.error("❌ Scheduler não foi inicializado")
        return False
    
    try:
        scheduler.remove_job(job_id)
        logger.info(f"✅ Tarefa '{job_id}' removida com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao remover tarefa '{job_id}': {e}")
        return False

def listar_tarefas():
    """
    Lista todas as tarefas agendadas
    
    Returns:
        list: Lista de informações das tarefas
    """
    global scheduler
    
    if scheduler is None:
        logger.error("❌ Scheduler não foi inicializado")
        return []
    
    try:
        jobs = scheduler.get_jobs()
        tarefas = []
        
        for job in jobs:
            tarefa_info = {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            }
            tarefas.append(tarefa_info)
        
        return tarefas
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar tarefas: {e}")
        return []

def pausar_scheduler():
    """
    Pausa o scheduler
    """
    global scheduler
    
    if scheduler is None:
        logger.error("❌ Scheduler não foi inicializado")
        return False
    
    try:
        scheduler.pause()
        logger.info("⏸️ Scheduler pausado")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao pausar scheduler: {e}")
        return False

def retomar_scheduler():
    """
    Retoma o scheduler
    """
    global scheduler
    
    if scheduler is None:
        logger.error("❌ Scheduler não foi inicializado")
        return False
    
    try:
        scheduler.resume()
        logger.info("▶️ Scheduler retomado")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao retomar scheduler: {e}")
        return False

def shutdown_scheduler():
    """
    Finaliza o scheduler de forma segura
    """
    global scheduler
    
    if scheduler is None:
        return
    
    try:
        scheduler.shutdown(wait=True)
        logger.info("🛑 Scheduler finalizado com sucesso")
        scheduler = None
        
    except Exception as e:
        logger.error(f"❌ Erro ao finalizar scheduler: {e}")

def get_scheduler():
    """
    Retorna a instância do scheduler
    
    Returns:
        BackgroundScheduler: Instância do scheduler ou None se não inicializado
    """
    return scheduler