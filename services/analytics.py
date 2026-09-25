from __future__ import annotations
from datetime import date, timedelta


def _parse(d):
    try:
        return date.fromisoformat(d)
    except Exception:
        return None


def trend(registros, chave='valor', dias=30):
    hoje = date.today()
    vals = []
    for r in registros:
        d = _parse(r.get('data', ''))
        if d and (hoje - d).days <= dias:
            try:
                vals.append((d, float(r[chave])))
            except (KeyError, TypeError, ValueError):
                pass
    vals.sort()
    if len(vals) < 2:
        return {'direcao': 'stable', 'variacao': 0.0, 'primeiro': None, 'ultimo': None, 'n': len(vals)}
    primeiro = vals[0][1]
    ultimo = vals[-1][1]
    return {
        'direcao': 'up' if ultimo > primeiro else 'down' if ultimo < primeiro else 'stable',
        'variacao': round(ultimo - primeiro, 2),
        'primeiro': primeiro,
        'ultimo': ultimo,
        'n': len(vals),
    }


def resumo(usuario):
    peso = trend(usuario.historico_peso, dias=30)
    glic = trend(usuario.historico_glicemia, dias=30)
    press = usuario.media_pressao_30dias()
    agua = round(usuario.progresso_agua(), 1)
    return {
        'peso': peso,
        'glicemia': glic,
        'pressao_media': press,
        'agua': agua,
        'registros': len(usuario.historico_peso) + len(usuario.historico_pressao) + len(usuario.historico_glicemia),
    }


def agua_7_dias(usuario):
    hoje = date.today()
    # agua_logs is loaded dynamically by the database helper when available.
    logs = getattr(usuario, 'agua_logs', []) or []
    out = []
    for i in range(6, -1, -1):
        d = hoje - timedelta(days=i)
        total = sum(float(x.get('quantidade', 0)) for x in logs if x.get('data') == d.isoformat())
        out.append({'data': d.isoformat(), 'litros': round(total, 2), 'meta': float(usuario.meta_agua)})
    return out


def calendar_month(year, month, agendamentos):
    import calendar
    cal = calendar.Calendar(firstweekday=0)
    eventos = {}
    for a in agendamentos:
        if a.get('status') != 'agendado':
            continue
        d = a.get('data_consulta')
        if d:
            eventos.setdefault(d, []).append(a)
    weeks = []
    for week in cal.monthdayscalendar(year, month):
        row = []
        for day in week:
            iso = f'{year:04d}-{month:02d}-{day:02d}' if day else None
            row.append({'day': day, 'date': iso, 'events': eventos.get(iso, []) if iso else []})
        weeks.append(row)
    return weeks
