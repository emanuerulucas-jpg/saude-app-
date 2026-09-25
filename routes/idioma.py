from flask import Blueprint, request, redirect, session, url_for
from utils.auth import login_obrigatorio
from services import usuario_service
from services.i18n import normalize_language

idioma_bp = Blueprint("idioma", __name__)

@idioma_bp.route("/idioma", methods=["POST"])
def alterar():
    idioma = normalize_language(request.form.get("idioma", "pt-BR"))
    session["idioma"] = idioma
    session["idioma_escolhido"] = True
    if session.get("login"):
        usuario_service.alterar_idioma(session["login"], idioma)
    return redirect(request.referrer or url_for("auth.index"))
