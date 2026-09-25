import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from utils.auth import login_obrigatorio

receitas_bp = Blueprint("receitas", __name__)


@receitas_bp.route("/receitas")
@login_obrigatorio
def listar():
    usuario = usuario_service.buscar_usuario(session["login"])
    return render_template("receitas.html", usuario=usuario)


@receitas_bp.route("/receitas/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar():
    medico = request.form["medico"]
    crm = request.form.get("crm", "")

    # Medicamentos chegam como listas paralelas
    nomes = request.form.getlist("med_nome")
    dosagens = request.form.getlist("med_dosagem")
    frequencias = request.form.getlist("med_frequencia")
    duracoes = request.form.getlist("med_duracao")

    medicamentos = [
        {"nome": n, "dosagem": d, "frequencia": f, "duracao": du}
        for n, d, f, du in zip(nomes, dosagens, frequencias, duracoes) if n
    ]

    ok, msg = usuario_service.adicionar_receita(session["login"], medico, crm, medicamentos)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("receitas.listar"))


@receitas_bp.route("/receitas/remover/<receita_id>", methods=["POST"])
@login_obrigatorio
def remover(receita_id):
    ok, msg = usuario_service.remover_receita(session["login"], receita_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("receitas.listar"))
