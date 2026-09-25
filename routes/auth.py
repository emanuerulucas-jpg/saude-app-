from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from services.i18n import translate

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return render_template("index.html")


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        ok, msg = usuario_service.cadastrar(
            login=request.form["login"],
            senha=request.form["senha"],
            nome=request.form["nome"],
            idade=request.form["idade"],
            altura=request.form["altura"],
            peso=request.form["peso"],
            tipo_sanguineo=request.form.get("tipo_sanguineo", ""),
            meta_agua=request.form.get("meta_agua", 2.0),
        )
        flash(msg, "success" if ok else "danger")
        if ok:
            return redirect(url_for("auth.login"))
    return render_template("cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = usuario_service.autenticar(
            request.form["login"], request.form["senha"])
        if usuario:
            session["login"] = usuario.login
            if not session.get("idioma_escolhido"):
                session["idioma"] = usuario.idioma
            return redirect(url_for("dashboard.dashboard"))
        flash(translate("auth.invalid_login"), "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
