import calendar
from datetime import date
from flask import Blueprint, render_template, request, session
from services import usuario_service
from services.analytics import calendar_month
from utils.auth import login_obrigatorio
from services.i18n import translate

calendario_bp = Blueprint('calendario', __name__)

@calendario_bp.route('/calendario')
@login_obrigatorio
def ver():
    hoje = date.today()
    try:
        year = int(request.args.get('ano', hoje.year)); month = int(request.args.get('mes', hoje.month))
        if not 1 <= month <= 12 or not 2000 <= year <= 2100: raise ValueError
    except ValueError:
        year, month = hoje.year, hoje.month
    prev_month = month - 1 if month > 1 else 12; prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1; next_year = year if month < 12 else year + 1
    usuario = usuario_service.buscar_usuario(session['login'])
    return render_template('calendario.html', usuario=usuario, weeks=calendar_month(year, month, usuario.agendamentos),
                           month_name=translate(f'calendar.month.{month}'), year=year,
                           weekdays=[translate(f'calendar.weekday.{i}') for i in range(7)],
                           prev_year=prev_year, prev_month=prev_month, next_year=next_year, next_month=next_month)
