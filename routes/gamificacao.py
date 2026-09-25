from flask import Blueprint, render_template, session
from services import gamificacao
from services.usuario_service import buscar_usuario
from utils.auth import login_obrigatorio

gamificacao_bp = Blueprint("gamificacao", __name__)


@gamificacao_bp.route("/gamificacao")
@login_obrigatorio
def pagina():
    login = session["login"]
    usuario = buscar_usuario(login)
    dados = gamificacao.resumo(login)
    return render_template("gamificacao.html", usuario=usuario, game=dados)
