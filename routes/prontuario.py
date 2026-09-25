from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from services.i18n import translate
from utils.auth import login_obrigatorio

prontuario_bp = Blueprint("prontuario", __name__)


@prontuario_bp.route("/prontuario")
@login_obrigatorio
def ver():
    usuario = usuario_service.buscar_usuario(session["login"])
    timeline = usuario.gerar_prontuario()
    return render_template("prontuario.html", usuario=usuario, timeline=timeline)


@prontuario_bp.route("/prontuario/atualizar", methods=["POST"])
@login_obrigatorio
def atualizar():
    def _para_lista(texto):
        return [x.strip() for x in texto.split(",") if x.strip()]

    usuario_service.atualizar_prontuario(
        session["login"],
        alergias=_para_lista(request.form.get("alergias", "")),
        doencas_cronicas=_para_lista(request.form.get("doencas_cronicas", "")),
        medicamentos_continuos=_para_lista(request.form.get("medicamentos_continuos", "")),
    )
    flash(translate("record.updated"), "success")
    return redirect(url_for("prontuario.ver"))
