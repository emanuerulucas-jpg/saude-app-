from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from utils.auth import login_obrigatorio

agendamentos_bp = Blueprint("agendamentos", __name__)


@agendamentos_bp.route("/agendamentos")
@login_obrigatorio
def listar():
    usuario = usuario_service.buscar_usuario(session["login"])
    futuros = sorted(usuario.agendamentos_futuros(), key=lambda a: (a["data_consulta"], a["hora"]))
    ids_futuros = {a["id"] for a in futuros}
    passados = sorted(
        [a for a in usuario.agendamentos if a["id"] not in ids_futuros],
        key=lambda a: (a.get("data_consulta",""), a.get("hora","")),
        reverse=True
    )
    return render_template("agendamentos.html", usuario=usuario,
                           futuros=futuros, passados=passados)


@agendamentos_bp.route("/agendamentos/criar", methods=["POST"])
@login_obrigatorio
def criar():
    dados = {
        "medico": request.form["medico"],
        "crm": request.form.get("crm", ""),
        "especialidade": request.form["especialidade"],
        "data_consulta": request.form["data_consulta"],
        "hora": request.form["hora"],
        "local": request.form.get("local", ""),
        "observacoes": request.form.get("observacoes", ""),
    }
    ok, msg = usuario_service.criar_agendamento(session["login"], dados)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("agendamentos.listar"))


@agendamentos_bp.route("/agendamentos/cancelar/<agendamento_id>", methods=["POST"])
@login_obrigatorio
def cancelar(agendamento_id):
    ok, msg = usuario_service.cancelar_agendamento(session["login"], agendamento_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("agendamentos.listar"))


@agendamentos_bp.route("/agendamentos/concluir/<agendamento_id>", methods=["POST"])
@login_obrigatorio
def concluir(agendamento_id):
    diagnostico = request.form.get("diagnostico", "")
    observacoes = request.form.get("observacoes", "")
    ok, msg = usuario_service.concluir_agendamento(session["login"], agendamento_id, diagnostico, observacoes)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("agendamentos.listar"))
