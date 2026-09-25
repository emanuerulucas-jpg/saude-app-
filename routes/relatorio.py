from flask import Blueprint, session, make_response
from services import usuario_service, relatorio_service
from utils.auth import login_obrigatorio

relatorio_bp = Blueprint("relatorio", __name__)


@relatorio_bp.route("/relatorio/pdf")
@login_obrigatorio
def gerar_pdf():
    usuario = usuario_service.buscar_usuario(session["login"])
    pdf_bytes = relatorio_service.gerar_pdf(usuario)

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = \
        f'attachment; filename="relatorio_{usuario.login}.pdf"'
    return response
