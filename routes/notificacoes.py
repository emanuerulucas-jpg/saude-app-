from flask import Blueprint, render_template, redirect, url_for, session, request
from database import banco
from services.notificacao_service import sincronizar
from services import usuario_service
from utils.auth import login_obrigatorio

notificacoes_bp = Blueprint('notificacoes', __name__)

@notificacoes_bp.route('/notificacoes')
@login_obrigatorio
def listar():
    usuario = usuario_service.buscar_usuario(session['login'])
    sincronizar(usuario)
    return render_template('notificacoes.html', notificacoes=banco.listar_notificacoes(session['login'], 100))

@notificacoes_bp.route('/notificacoes/<int:notificacao_id>/ler', methods=['POST'])
@login_obrigatorio
def ler(notificacao_id):
    banco.marcar_notificacao_lida(session['login'], notificacao_id)
    return redirect(request.referrer or url_for('notificacoes.listar'))

@notificacoes_bp.route('/notificacoes/ler-todas', methods=['POST'])
@login_obrigatorio
def ler_todas():
    banco.marcar_todas_lidas(session['login'])
    return redirect(url_for('notificacoes.listar'))
