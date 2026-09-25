import json
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service
from utils.auth import login_obrigatorio
from services.analytics import resumo, agua_7_dias
from services.notificacao_service import sincronizar
from services.i18n import translate

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_obrigatorio
def dashboard():
    usuario = usuario_service.buscar_usuario(session["login"])
    from services import gamificacao
    gamificacao.sync_profile(session["login"], usuario)
    alertas = usuario.gerar_alertas()
    sincronizar(usuario)
    analytics = resumo(usuario)
    agua_semana = agua_7_dias(usuario)
    media_pressao = usuario.media_pressao_30dias()

    # Dados para Chart.js (últimos 15 registros)
    graf_peso = {
        "labels": [p["data"] for p in usuario.historico_peso[-15:]],
        "dados": [p["valor"] for p in usuario.historico_peso[-15:]],
    }
    graf_sistolica = {
        "labels": [p["data"] for p in usuario.historico_pressao[-15:]],
        "dados_sis": [p["sistolica"] for p in usuario.historico_pressao[-15:]],
        "dados_dia": [p["diastolica"] for p in usuario.historico_pressao[-15:]],
    }
    graf_glicemia = {
        "labels": [g["data"] for g in usuario.historico_glicemia[-15:]],
        "dados": [g["valor"] for g in usuario.historico_glicemia[-15:]],
    }

    return render_template("dashboard.html",
                           usuario=usuario,
                           alertas=alertas,
                           media_pressao=media_pressao,
                           graf_peso=json.dumps(graf_peso),
                           graf_pressao=json.dumps(graf_sistolica),
                           graf_glicemia=json.dumps(graf_glicemia),
                           analytics=analytics, agua_semana=agua_semana)


# ── Hidratação ──────────────────────────────────────────
@dashboard_bp.route("/agua/adicionar", methods=["POST"])
@login_obrigatorio
def adicionar_agua():
    sucesso, mensagem = usuario_service.adicionar_agua(
        session["login"], request.form.get("quantidade", "")
    )
    if sucesso:
        flash(translate("dash.water_added"), "success")
    else:
        flash(mensagem, "danger")
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/agua/resetar")
@login_obrigatorio
def resetar_agua():
    usuario_service.resetar_agua(session["login"])
    return redirect(url_for("dashboard.dashboard"))


# ── Registros de saúde ──────────────────────────────────
@dashboard_bp.route("/peso/registrar", methods=["POST"])
@login_obrigatorio
def registrar_peso():
    sucesso, mensagem = usuario_service.registrar_peso(
        session["login"], request.form.get("valor", "")
    )
    flash(mensagem, "success" if sucesso else "danger")
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/pressao/registrar", methods=["POST"])
@login_obrigatorio
def registrar_pressao():
    sucesso, mensagem = usuario_service.registrar_pressao(
        session["login"],
        request.form.get("sistolica", ""),
        request.form.get("diastolica", "")
    )
    flash(mensagem, "success" if sucesso else "danger")
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/glicemia/registrar", methods=["POST"])
@login_obrigatorio
def registrar_glicemia():
    sucesso, mensagem = usuario_service.registrar_glicemia(
        session["login"], request.form.get("valor", "")
    )
    flash(mensagem, "success" if sucesso else "danger")
    return redirect(url_for("dashboard.dashboard"))
