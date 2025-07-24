from flask import Blueprint, jsonify, request
from app.scheduler import (
    listar_tarefas, 
    pausar_scheduler, 
    retomar_scheduler,
    adicionar_tarefa,
    remover_tarefa,
    get_scheduler
)
from app.service.limpeza_usuarios_expirados import limpar_usuarios_expirados
import logging

logger = logging.getLogger(__name__)

scheduler_admin_bp = Blueprint('scheduler_admin', __name__)

@scheduler_admin_bp.route('/admin/scheduler/status', methods=['GET'])
def status_scheduler():
    """
    Retorna o status atual do scheduler
    """
    try:
        scheduler = get_scheduler()
        
        if scheduler is None:
            return jsonify({
                "status": "error",
                "mensagem": "Scheduler não foi inicializado",
                "ativo": False
            }), 500
        
        status_info = {
            "status": "success",
            "ativo": scheduler.running,
            "estado": "executando" if scheduler.running else "parado",
            "total_tarefas": len(scheduler.get_jobs())
        }
        
        return jsonify(status_info), 200
        
    except Exception as e:
        logger.error(f"Erro ao obter status do scheduler: {e}")
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao obter status: {str(e)}"
        }), 500

@scheduler_admin_bp.route('/admin/scheduler/tarefas', methods=['GET'])
def listar_tarefas_agendadas():
    """
    Lista todas as tarefas agendadas
    """
    try:
        tarefas = listar_tarefas()
        
        return jsonify({
            "status": "success",
            "total_tarefas": len(tarefas),
            "tarefas": tarefas
        }), 200
        
    except Exception as e:
        logger.error(f"Erro ao listar tarefas: {e}")
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao listar tarefas: {str(e)}"
        }), 500

@scheduler_admin_bp.route('/admin/scheduler/pausar', methods=['POST'])
def pausar():
    """
    Pausa o scheduler
    """
    try:
        sucesso = pausar_scheduler()
        
        if sucesso:
            return jsonify({
                "status": "success",
                "mensagem": "Scheduler pausado com sucesso"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "mensagem": "Falha ao pausar scheduler"
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao pausar scheduler: {e}")
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao pausar scheduler: {str(e)}"
        }), 500

@scheduler_admin_bp.route('/admin/scheduler/retomar', methods=['POST'])
def retomar():
    """
    Retoma o scheduler
    """
    try:
        sucesso = retomar_scheduler()
        
        if sucesso:
            return jsonify({
                "status": "success",
                "mensagem": "Scheduler retomado com sucesso"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "mensagem": "Falha ao retomar scheduler"
            }), 500
            
    except Exception as e:
        logger.error(f"Erro ao retomar scheduler: {e}")
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao retomar scheduler: {str(e)}"
        }), 500

@scheduler_admin_bp.route('/admin/scheduler/executar-limpeza', methods=['POST'])
def executar_limpeza_manual():
    """
    Executa manualmente a limpeza de usuários expirados
    """
    try:
        resultado = limpar_usuarios_expirados()
        
        if resultado["sucesso"]:
            return jsonify({
                "status": "success",
                "mensagem": resultado["mensagem"],
                "usuarios_removidos": resultado["usuarios_removidos"]
            }), 200
        else:
            return jsonify({
                "status": "warning",
                "mensagem": resultado["mensagem"],
                "usuarios_removidos": resultado["usuarios_removidos"]
            }), 200
            
    except Exception as e:
        logger.error(f"Erro ao executar limpeza manual: {e}")
        return jsonify({
            "status": "error",
            "mensagem": f"Erro ao executar limpeza: {str(e)}"
        }), 500