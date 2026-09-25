import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, send_from_directory
from services import usuario_service
from utils.auth import login_obrigatorio, extensao_permitida
from werkzeug.utils import secure_filename

exames_bp = Blueprint("exames", __name__)


@exames_bp.route("/exames")
@login_obrigatorio
def listar():
    usuario = usuario_service.buscar_usuario(session["login"])
    return render_template("exames.html", usuario=usuario)


@exames_bp.route("/exames/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar():
    tipo = request.form["tipo"]
    resultado = request.form.get("resultado", "")
    observacoes = request.form.get("observacoes", "")
    arquivo_nome = None

    arquivo = request.files.get("arquivo")
    if arquivo and arquivo.filename and extensao_permitida(arquivo.filename):
        ext = arquivo.filename.rsplit(".", 1)[1].lower()
        arquivo_nome = f"{uuid.uuid4().hex[:8]}_{secure_filename(tipo)[:60]}.{ext}"
        pasta = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(pasta, exist_ok=True)
        arquivo.save(os.path.join(pasta, arquivo_nome))

    ok, msg = usuario_service.adicionar_exame(session["login"], tipo, resultado, observacoes, arquivo_nome)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("exames.listar"))


@exames_bp.route("/exames/remover/<exame_id>", methods=["POST"])
@login_obrigatorio
def remover(exame_id):
    ok, msg = usuario_service.remover_exame(session["login"], exame_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("exames.listar"))


@exames_bp.route("/exames/arquivo/<nome>")
@login_obrigatorio
def ver_arquivo(nome):
    pasta = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(pasta, nome)
