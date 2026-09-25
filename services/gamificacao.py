from __future__ import annotations
from datetime import date, timedelta
from database import banco

XP_VALUES = {
    "perfil_completo": 50, "registro_peso": 10, "registro_pressao": 10,
    "registro_glicemia": 10, "agua_adicao": 2, "meta_agua": 20,
    "consulta": 20, "receita": 10, "exame": 15, "agendamento": 15,
}

ACHIEVEMENTS = {
    "primeiro_passo": {"title": "Primeiro passo", "description": "Faça seu primeiro registro no SaúdeApp.", "xp": 25, "icon": "◆"},
    "constancia_7": {"title": "7 dias de constância", "description": "Use o acompanhamento em 7 dias diferentes.", "xp": 75, "icon": "7"},
    "constancia_30": {"title": "30 dias de constância", "description": "Use o acompanhamento em 30 dias diferentes.", "xp": 200, "icon": "30"},
    "hidratacao_7": {"title": "Hidratação em dia", "description": "Alcance sua meta de água em 7 dias diferentes.", "xp": 100, "icon": "W"},
    "dez_registros": {"title": "Diário ativo", "description": "Faça 10 registros de acompanhamento.", "xp": 75, "icon": "10"},
    "perfil": {"title": "Perfil completo", "description": "Mantenha os dados básicos do perfil preenchidos.", "xp": 50, "icon": "✓"},
}

RANKS = [
    (1, "Iniciante", "Você começou a construir seu histórico."),
    (3, "Constante", "Seu acompanhamento já virou rotina."),
    (5, "Organizado", "Você está mantendo seus registros em dia."),
    (8, "Disciplinado", "Sua constância já faz diferença no histórico."),
    (12, "Veterano", "Você construiu um histórico consistente."),
    (16, "Referência", "Seu perfil demonstra uma longa sequência de acompanhamento."),
    (20, "Mestre do acompanhamento", "Um longo histórico de organização e constância."),
]

REWARDS = [
    (2, "Título: Constante", "Desbloqueado ao alcançar o nível 2."),
    (3, "Título: Organizado", "Desbloqueado ao alcançar o nível 3."),
    (5, "Título: Disciplinado", "Desbloqueado ao alcançar o nível 5."),
    (7, "Tema de perfil: Safira", "Desbloqueado ao alcançar o nível 7."),
    (10, "Título: Veterano", "Desbloqueado ao alcançar o nível 10."),
    (15, "Tema de perfil: Grafite", "Desbloqueado ao alcançar o nível 15."),
]


def _level_for_xp(xp: int) -> int:
    level = 1
    threshold = 0
    while xp >= threshold + level * 100:
        threshold += level * 100
        level += 1
    return level


def _thresholds(level: int):
    current = 0
    for n in range(1, level):
        current += n * 100
    return current, current + level * 100


def _ensure(login):
    banco.inicializar()
    with banco._db() as db:
        db.execute("INSERT OR IGNORE INTO gamificacao(usuario_login,xp) VALUES(?,0)", (login,))


def award(login, chave, tipo, xp, descricao):
    _ensure(login)
    hoje = date.today().isoformat()
    with banco._db() as db:
        cur = db.execute(
            "INSERT OR IGNORE INTO gamificacao_eventos(usuario_login,chave,tipo,xp,data,descricao) VALUES(?,?,?,?,?,?)",
            (login, chave, tipo, xp, hoje, descricao),
        )
        if cur.rowcount == 0:
            return {"added": 0, "new_achievements": []}
        db.execute("UPDATE gamificacao SET xp=xp+? WHERE usuario_login=?", (xp, login))
    return {"added": xp, "new_achievements": check_achievements(login)}


def register_action(login, action, unique_key=None):
    xp = XP_VALUES.get(action, 0)
    if xp <= 0:
        return {"added": 0, "new_achievements": []}
    today = date.today().isoformat()
    key = unique_key or f"{action}:{today}"
    descriptions = {
        "perfil_completo": "Perfil básico preenchido", "registro_peso": "Registro de peso",
        "registro_pressao": "Registro de pressão", "registro_glicemia": "Registro de glicemia",
        "agua_adicao": "Registro de hidratação", "meta_agua": "Meta diária de hidratação alcançada",
        "consulta": "Consulta registrada", "receita": "Receita registrada", "exame": "Exame registrado",
        "agendamento": "Consulta agendada",
    }
    return award(login, key, action, xp, descriptions.get(action, "Atividade registrada"))


def _activity_dates(login):
    with banco._db() as db:
        rows = db.execute("SELECT DISTINCT data FROM gamificacao_eventos WHERE usuario_login=? ORDER BY data", (login,)).fetchall()
    return {r[0] for r in rows}


def current_streak(login):
    dates = _activity_dates(login)
    if not dates:
        return 0
    cursor = date.today()
    if cursor.isoformat() not in dates:
        cursor -= timedelta(days=1)
    streak = 0
    while cursor.isoformat() in dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def best_streak(login):
    dates = sorted(date.fromisoformat(d) for d in _activity_dates(login))
    best = cur = 0
    previous = None
    for d in dates:
        if previous and d == previous + timedelta(days=1):
            cur += 1
        else:
            cur = 1
        best = max(best, cur)
        previous = d
    return best


def _total_events(login):
    with banco._db() as db:
        return db.execute("SELECT COUNT(*) AS n FROM gamificacao_eventos WHERE usuario_login=?", (login,)).fetchone()["n"]


def _water_goal_days(login):
    with banco._db() as db:
        return db.execute("SELECT COUNT(DISTINCT chave) AS n FROM gamificacao_eventos WHERE usuario_login=? AND tipo='meta_agua'", (login,)).fetchone()["n"]


def check_achievements(login):
    _ensure(login)
    with banco._db() as db:
        earned = {r[0] for r in db.execute("SELECT codigo FROM gamificacao_conquistas WHERE usuario_login=?", (login,))}
    candidates = []
    if _total_events(login) >= 1: candidates.append("primeiro_passo")
    if len(_activity_dates(login)) >= 7: candidates.append("constancia_7")
    if len(_activity_dates(login)) >= 30: candidates.append("constancia_30")
    if _water_goal_days(login) >= 7: candidates.append("hidratacao_7")
    if _total_events(login) >= 10: candidates.append("dez_registros")
    new = []
    for code in candidates:
        if code in earned:
            continue
        info = ACHIEVEMENTS[code]
        with banco._db() as db:
            cur = db.execute("INSERT OR IGNORE INTO gamificacao_conquistas(usuario_login,codigo,desbloqueada_em) VALUES(?,?,CURRENT_TIMESTAMP)", (login, code))
            if cur.rowcount:
                db.execute("UPDATE gamificacao SET xp=xp+? WHERE usuario_login=?", (info["xp"], login))
                new.append(code)
    return new


def profile_complete(usuario):
    return bool(usuario.nome.strip() and usuario.idade > 0 and usuario.altura > 0 and usuario.peso > 0 and usuario.tipo_sanguineo.strip())


def sync_profile(login, usuario):
    if not profile_complete(usuario):
        return {"added": 0, "new_achievements": []}
    result = register_action(login, "perfil_completo", "perfil_completo")
    with banco._db() as db:
        row = db.execute("SELECT 1 FROM gamificacao_conquistas WHERE usuario_login=? AND codigo='perfil'", (login,)).fetchone()
        if not row:
            db.execute("INSERT OR IGNORE INTO gamificacao_conquistas(usuario_login,codigo,desbloqueada_em) VALUES(?,?,CURRENT_TIMESTAMP)", (login, "perfil"))
    return result


def daily_missions(login):
    today = date.today().isoformat()
    with banco._db() as db:
        rows = db.execute("SELECT tipo, COUNT(*) AS n FROM gamificacao_eventos WHERE usuario_login=? AND data=? GROUP BY tipo", (login, today)).fetchall()
    counts = {r[0]: r[1] for r in rows}
    tracking = counts.get("registro_peso", 0) + counts.get("registro_pressao", 0) + counts.get("registro_glicemia", 0)
    return [
        {"id":"acompanhamento", "title":"Atualize seu acompanhamento", "description":"Faça pelo menos 1 registro de saúde hoje.", "progress": min(tracking, 1), "target": 1},
        {"id":"hidratacao", "title":"Registre sua hidratação", "description":"Adicione pelo menos um registro de água hoje.", "progress": min(counts.get("agua_adicao", 0), 1), "target": 1},
        {"id":"organizacao", "title":"Mantenha seus registros organizados", "description":"Registre uma consulta, exame, receita ou agendamento.", "progress": min(counts.get("consulta", 0) + counts.get("exame", 0) + counts.get("receita", 0) + counts.get("agendamento", 0), 1), "target": 1},
    ]


def weekly_missions(login):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    with banco._db() as db:
        rows = db.execute("SELECT tipo, data FROM gamificacao_eventos WHERE usuario_login=? AND data>=?", (login, monday.isoformat())).fetchall()
    tracking_types = {"registro_peso", "registro_pressao", "registro_glicemia"}
    tracking_days = len({r[1] for r in rows if r[0] in tracking_types})
    water = sum(1 for r in rows if r[0] == "agua_adicao")
    organization = sum(1 for r in rows if r[0] in {"consulta", "exame", "receita", "agendamento"})
    return [
        {"id":"semana_acompanhamento", "title":"Semana consistente", "description":"Registre seu acompanhamento em 3 dias diferentes nesta semana.", "progress": min(tracking_days, 3), "target": 3, "xp": 30},
        {"id":"semana_hidratacao", "title":"Rotina de hidratação", "description":"Faça 5 registros de água durante a semana.", "progress": min(water, 5), "target": 5, "xp": 30},
        {"id":"semana_organizacao", "title":"Semana organizada", "description":"Registre 2 consultas, exames, receitas ou agendamentos.", "progress": min(organization, 2), "target": 2, "xp": 30},
    ]


def sync_weekly_rewards(login):
    missions = weekly_missions(login)
    monday = date.today() - timedelta(days=date.today().weekday())
    week_key = monday.isoformat()
    awarded = []
    for mission in missions:
        if mission["progress"] >= mission["target"]:
            result = award(login, f"semana:{week_key}:{mission['id']}", "missao_semanal", mission["xp"], f"Missão semanal: {mission['title']}")
            if result["added"]:
                awarded.append(mission["id"])
    if all(m["progress"] >= m["target"] for m in missions):
        result = award(login, f"semana:{week_key}:completa", "semana_completa", 100, "Bônus por completar todas as missões semanais")
        if result["added"]:
            awarded.append("completa")
    return awarded


def _rank(level):
    chosen = RANKS[0]
    for item in RANKS:
        if level >= item[0]:
            chosen = item
    return {"level": chosen[0], "title": chosen[1], "description": chosen[2]}


def _rewards(level):
    return [{"level": lvl, "title": title, "description": desc, "unlocked": level >= lvl} for lvl, title, desc in REWARDS]


def _skill_tree(login):
    with banco._db() as db:
        rows = db.execute("SELECT tipo, COUNT(*) AS n FROM gamificacao_eventos WHERE usuario_login=? GROUP BY tipo", (login,)).fetchall()
    counts = {r[0]: r[1] for r in rows}
    nodes = [
        ("registro", "Registro", "Peso, pressão e glicemia", counts.get("registro_peso",0)+counts.get("registro_pressao",0)+counts.get("registro_glicemia",0), 5),
        ("agua", "Hidratação", "Acompanhamento de água", counts.get("agua_adicao",0), 5),
        ("organizacao", "Organização", "Consultas, exames e receitas", counts.get("consulta",0)+counts.get("exame",0)+counts.get("receita",0)+counts.get("agendamento",0), 5),
        ("constancia", "Constância", "Dias diferentes com atividade", len(_activity_dates(login)), 7),
    ]
    return [{"id": i, "title": title, "description": desc, "value": min(value, target), "target": target, "percent": round(min(value/target,1)*100)} for i,title,desc,value,target in nodes]


def resumo(login):
    _ensure(login)
    sync_weekly_rewards(login)
    check_achievements(login)
    with banco._db() as db:
        xp = db.execute("SELECT xp FROM gamificacao WHERE usuario_login=?", (login,)).fetchone()["xp"]
        events = db.execute("SELECT tipo,xp,data,descricao FROM gamificacao_eventos WHERE usuario_login=? ORDER BY id DESC LIMIT 12", (login,)).fetchall()
        earned = db.execute("SELECT codigo,desbloqueada_em FROM gamificacao_conquistas WHERE usuario_login=? ORDER BY id DESC", (login,)).fetchall()
    level = _level_for_xp(xp)
    current, nxt = _thresholds(level)
    earned_codes = {r[0] for r in earned}
    return {
        "xp": xp, "level": level, "current_level_xp": current, "next_level_xp": nxt,
        "progress": round(((xp-current)/(nxt-current))*100, 1) if nxt > current else 100,
        "streak": current_streak(login), "best_streak": best_streak(login),
        "total_events": _total_events(login), "water_goal_days": _water_goal_days(login),
        "rank": _rank(level), "rewards": _rewards(level),
        "achievements": [{"codigo": r[0], "desbloqueada_em": r[1], **ACHIEVEMENTS.get(r[0], {})} for r in earned],
        "locked": [{"codigo": c, **info} for c, info in ACHIEVEMENTS.items() if c not in earned_codes],
        "recent": [dict(r) for r in events], "missions": daily_missions(login),
        "weekly_missions": weekly_missions(login), "skill_tree": _skill_tree(login),
        "rewards_unlocked": sum(1 for r in REWARDS if level >= r[0]), "rewards_total": len(REWARDS),
    }
