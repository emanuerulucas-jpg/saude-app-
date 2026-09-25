import secrets
from functools import wraps
from flask import session, request, abort


def token():
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_urlsafe(32)
    return session['_csrf']


def validar():
    esperado = session.get('_csrf')
    recebido = request.form.get('_csrf') or request.headers.get('X-CSRF-Token')
    if not esperado or not recebido or not secrets.compare_digest(esperado, recebido):
        abort(400, description='Token de segurança inválido. Recarregue a página e tente novamente.')


def csrf_protect(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        validar()
        return f(*args, **kwargs)
    return wrapper
