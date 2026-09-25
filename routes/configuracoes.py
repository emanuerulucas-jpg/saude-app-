from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services import usuario_service, relatorio_service
from utils.auth import login_obrigatorio

config_bp = Blueprint('configuracoes', __name__)

@config_bp.route('/configuracoes')
@login_obrigatorio
def pagina():
    return render_template('configuracoes.html', usuario=usuario_service.buscar_usuario(session['login']))

@config_bp.route('/configuracoes/senha', methods=['POST'])
@login_obrigatorio
def senha():
    ok, msg = usuario_service.alterar_senha(session['login'], request.form.get('senha_atual',''), request.form.get('nova_senha',''))
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('configuracoes.pagina'))

@config_bp.route('/configuracoes/exportar')
@login_obrigatorio
def exportar():
    """Gera o relatório de saúde em PDF para download."""
    usuario = usuario_service.buscar_usuario(session['login'])
    pdf_bytes = relatorio_service.gerar_pdf(usuario)

    from flask import make_response
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = (
        f'attachment; filename="SaudeApp_relatorio_{usuario.login}.pdf"'
    )
    return response
