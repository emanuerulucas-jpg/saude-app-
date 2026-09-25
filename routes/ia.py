from flask import Blueprint, render_template, request, session, flash
from utils.auth import login_obrigatorio
from services import usuario_service
from services.ai_service import perguntar

ia_bp = Blueprint("ia", __name__)

@ia_bp.route("/assistente")
@login_obrigatorio
def pagina():
    usuario = usuario_service.buscar_usuario(session["login"])
    return render_template("ia.html", usuario=usuario)

@ia_bp.route("/assistente/perguntar", methods=["POST"])
@login_obrigatorio
def perguntar_ia():
    usuario = usuario_service.buscar_usuario(session["login"])
    pergunta = request.form.get("pergunta", "")
    ok, resposta = perguntar(usuario, pergunta, usuario.idioma)
    return render_template("ia.html", usuario=usuario, pergunta=pergunta, resposta=resposta, resposta_ok=ok)
