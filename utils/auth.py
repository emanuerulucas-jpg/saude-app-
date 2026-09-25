from functools import wraps
from flask import session, redirect, url_for

EXTENSOES_PERMITIDAS = {"pdf", "png", "jpg", "jpeg"}


def login_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "login" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def extensao_permitida(nome_arquivo: str) -> bool:
    return "." in nome_arquivo and \
           nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
