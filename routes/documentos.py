from flask import Blueprint, render_template, session, redirect, url_for, flash, make_response, request
from services import usuario_service
from services.i18n import translate
from services import documento_service
from database import banco
from utils.auth import login_obrigatorio

documentos_bp=Blueprint("documentos",__name__)

@documentos_bp.route("/documentos")
@login_obrigatorio
def listar():
    usuario=usuario_service.buscar_usuario(session["login"])
    return render_template("documentos.html",usuario=usuario)


def _pdf(data,nome):
    r=make_response(data); r.headers["Content-Type"]="application/pdf"; r.headers["Content-Disposition"]=f'inline; filename="{nome}"'; return r


@documentos_bp.route("/documentos/carteirinha.pdf")
@login_obrigatorio
def carteirinha():
    u=usuario_service.buscar_usuario(session["login"]); token=documento_service.criar_token(u.login,"carteirinha"); url=url_for("documentos.verificar",token=token,_external=True)
    return _pdf(documento_service.gerar_carteirinha(u,url),"carteirinha_simulada.pdf")

@documentos_bp.route("/documentos/resumo.pdf")
@login_obrigatorio
def resumo():
    u=usuario_service.buscar_usuario(session["login"]); token=documento_service.criar_token(u.login,"resumo"); url=url_for("documentos.verificar",token=token,_external=True); return _pdf(documento_service.gerar_resumo(u,url),"resumo_saude_simulado.pdf")

@documentos_bp.route("/documentos/receita/<receita_id>.pdf")
@login_obrigatorio
def receita(receita_id):
    u=usuario_service.buscar_usuario(session["login"]); r=next((x for x in u.receitas if x["id"]==receita_id),None)
    if not r: flash(translate("docs.prescription_not_found"),"danger"); return redirect(url_for("documentos.listar"))
    token=documento_service.criar_token(u.login,"receita",r["id"]); url=url_for("documentos.verificar",token=token,_external=True); return _pdf(documento_service.gerar_receita(u,r,url),f"receita_{r['id']}_simulada.pdf")

@documentos_bp.route("/documentos/agendamento/<agendamento_id>.pdf")
@login_obrigatorio
def agendamento(agendamento_id):
    u=usuario_service.buscar_usuario(session["login"]); a=next((x for x in u.agendamentos if x["id"]==agendamento_id),None)
    if not a: flash(translate("docs.appointment_not_found"),"danger"); return redirect(url_for("documentos.listar"))
    token=documento_service.criar_token(u.login,"agendamento",a["id"]); url=url_for("documentos.verificar",token=token,_external=True); return _pdf(documento_service.gerar_agendamento(u,a,url),f"agendamento_{a['id']}_simulado.pdf")

@documentos_bp.route("/documentos/exame/<exame_id>.pdf")
@login_obrigatorio
def exame(exame_id):
    u=usuario_service.buscar_usuario(session["login"]); e=next((x for x in u.exames if x["id"]==exame_id),None)
    if not e: flash(translate("docs.exam_not_found"),"danger"); return redirect(url_for("documentos.listar"))
    token=documento_service.criar_token(u.login,"exame",e["id"]); url=url_for("documentos.verificar",token=token,_external=True); return _pdf(documento_service.gerar_exame(u,e,url),f"exame_{e['id']}_simulado.pdf")

@documentos_bp.route("/documentos/verificar/<token>")
def verificar(token):
    doc=banco.buscar_documento(token)
    if not doc: return render_template("erro.html",codigo=404,mensagem=translate("docs.document_not_found")) ,404
    return render_template("documento_verificacao.html",documento=doc)
