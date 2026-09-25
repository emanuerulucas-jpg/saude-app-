from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, current_app
from services import usuario_service
from services.i18n import translate
from database import banco
from utils.auth import login_obrigatorio
from werkzeug.utils import secure_filename
import os
import uuid

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/perfil")
@login_obrigatorio
def perfil():
    usuario = usuario_service.buscar_usuario(session["login"])
    return render_template("perfil.html", usuario=usuario)


@perfil_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_perfil():
    usuario = usuario_service.buscar_usuario(session["login"])
    if request.method == "POST":
        campos = {
            "nome": request.form.get("nome", ""), "idade": request.form.get("idade", ""),
            "altura": request.form.get("altura", ""), "peso": request.form.get("peso", ""),
            "tipo_sanguineo": request.form.get("tipo_sanguineo", ""),
            "meta_agua": request.form.get("meta_agua", ""), "observacoes": request.form.get("observacoes", ""),
        }
        ok, msg = usuario_service.atualizar_perfil(session["login"], campos)

        if ok:
            foto = request.files.get("foto_perfil")
            if foto and foto.filename:
                extensao = foto.filename.rsplit(".", 1)[-1].lower() if "." in foto.filename else ""
                permitidas = {"jpg", "jpeg", "png", "webp"}

                if extensao not in permitidas:
                    flash(translate("profile.photo_invalid"), "danger")
                    return redirect(url_for("perfil.editar_perfil"))

                nome_arquivo = secure_filename(f"{session['login']}_{uuid.uuid4().hex}.{extensao}")
                pasta = current_app.config["UPLOAD_FOLDER"]
                os.makedirs(pasta, exist_ok=True)
                caminho = os.path.join(pasta, nome_arquivo)
                foto.save(caminho)

                # Remove a foto anterior para não acumular arquivos.
                if usuario.foto_perfil:
                    anterior = os.path.join(pasta, os.path.basename(usuario.foto_perfil))
                    if os.path.isfile(anterior) and anterior != caminho:
                        os.remove(anterior)

                usuario.foto_perfil = nome_arquivo
                banco.salvar_usuario(usuario.para_dict())

            flash(msg, "success")
            return redirect(url_for("perfil.perfil"))

        flash(msg, "danger")

    return render_template("editar_perfil.html", usuario=usuario)


@perfil_bp.route("/perfil/foto")
@login_obrigatorio
def foto_perfil():
    usuario = usuario_service.buscar_usuario(session["login"])
    if not usuario or not usuario.foto_perfil:
        return ("", 404)
    pasta = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(pasta, os.path.basename(usuario.foto_perfil))


@perfil_bp.route("/perfil/deletar", methods=["POST"])
@login_obrigatorio
def deletar_conta():
    usuario_service.deletar_conta(session["login"])
    session.clear()
    flash(translate("profile.account_deleted"), "info")
    return redirect(url_for("auth.index"))
