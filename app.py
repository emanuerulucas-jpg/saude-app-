import os
import secrets
from flask import Flask, render_template, request, session
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.perfil import perfil_bp
from routes.consultas import consultas_bp
from routes.receitas import receitas_bp
from routes.exames import exames_bp
from routes.relatorio import relatorio_bp
from routes.agendamentos import agendamentos_bp
from routes.prontuario import prontuario_bp
from routes.documentos import documentos_bp
from routes.idioma import idioma_bp
from routes.ia import ia_bp
from routes.notificacoes import notificacoes_bp
from routes.calendario import calendario_bp
from routes.configuracoes import config_bp
from routes.gamificacao import gamificacao_bp
from services.i18n import translate, language_names, get_language, notification_localized
from utils.csrf import token, validar
from database import banco

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def criar_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_HTTPS", "0") == "1"

    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

    banco.inicializar_e_migrar()

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(perfil_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(receitas_bp)
    app.register_blueprint(exames_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(prontuario_bp)
    app.register_blueprint(documentos_bp)
    app.register_blueprint(idioma_bp)
    app.register_blueprint(ia_bp)
    app.register_blueprint(notificacoes_bp)
    app.register_blueprint(calendario_bp)
    app.register_blueprint(config_bp)
    app.register_blueprint(gamificacao_bp)

    # CSRF para todas as requisições que alteram dados.
    @app.before_request
    def proteger_mutacoes():
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            validar()

    @app.context_processor
    def contexto_global():
        from utils.tempo import agora as agora_local
        agora = agora_local()
        return {
            "t": translate,
            "idioma_atual": get_language(),
            "idiomas": language_names(),
            "agora": agora,
            "data_hoje": agora.strftime("%Y-%m-%d"),
            "data_hoje_br": agora.strftime("%d/%m/%Y"),
            "csrf_token": token,
            "notificacoes_nao_lidas": banco.contar_nao_lidas(session["login"]) if session.get("login") else 0,
            "usuario_atual": __import__("services.usuario_service", fromlist=["buscar_usuario"]).buscar_usuario(session["login"]) if session.get("login") else None,
            "gamificacao_atual": __import__("services.gamificacao", fromlist=["resumo"]).resumo(session["login"]) if session.get("login") else None,
            "notification_localized": notification_localized,
        }

    @app.errorhandler(404)
    def pagina_404(_):
        return render_template("erro.html", codigo=404, mensagem=translate("errors.not_found")), 404

    @app.errorhandler(413)
    def arquivo_grande(_):
        return render_template("erro.html", codigo=413, mensagem=translate("errors.file_too_large")), 413

    @app.errorhandler(500)
    def erro_interno(_):
        return render_template("erro.html", codigo=500, mensagem=translate("errors.internal")), 500

    return app


if __name__ == "__main__":
    app = criar_app()
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
