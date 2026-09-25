from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from utils.auth import login_obrigatorio

consultas_bp = Blueprint("consultas", __name__)


@consultas_bp.route("/consultas")
@login_obrigatorio
def listar():
    usuario = usuario_service.buscar_usuario(session["login"])
    return render_template("consultas.html", usuario=usuario)


@consultas_bp.route("/consultas/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar():
    dados = {
        "medico": request.form["medico"],
        "crm": request.form.get("crm", ""),
        "especialidade": request.form["especialidade"],
        "diagnostico": request.form.get("diagnostico", ""),
        "observacoes": request.form.get("observacoes", ""),
        "data": request.form.get("data", ""),
    }
    ok, msg = usuario_service.adicionar_consulta(session["login"], dados)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("consultas.listar"))


@consultas_bp.route("/consultas/remover/<consulta_id>", methods=["POST"])
@login_obrigatorio
def remover(consulta_id):
    ok, msg = usuario_service.remover_consulta(session["login"], consulta_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("consultas.listar"))
