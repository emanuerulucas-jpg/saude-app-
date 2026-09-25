from services.i18n import translate
"""
Service de Usuário — lógica de negócio entre as rotas e o banco.
Nunca expõe objetos internos diretamente; retorna dicts ou objetos Usuario.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Usuario
from database import banco


# ──────────────────────────────────────────
# Auth
# ──────────────────────────────────────────

def cadastrar(login, senha, nome, idade, altura, peso,
              tipo_sanguineo="", meta_agua=2.0):
    if banco.login_existe(login):
        return False, translate("auth.login_exists")

    try:
        idade = int(idade)
        altura = float(altura)
        peso = float(peso)
        meta_agua = float(meta_agua)
    except (ValueError, TypeError):
        return False, translate("register.invalid_numbers")

    if not 0 <= idade <= 120:
        return False, translate("register.invalid_age")
    if not 0.5 <= altura <= 2.5:
        return False, translate("register.invalid_height")
    if not 1 <= peso <= 500:
        return False, translate("register.invalid_weight")
    if not 0.5 <= meta_agua <= 10:
        return False, translate("register.invalid_water")

    usuario = Usuario(
        login=login,
        senha=generate_password_hash(senha),
        nome=nome,
        idade=idade,
        altura=altura,
        peso=peso,
        tipo_sanguineo=tipo_sanguineo,
        meta_agua=meta_agua,
    )
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.sync_profile(login, usuario)
    return True, translate("register.success")


def autenticar(login, senha):
    dados = banco.buscar_usuario(login)
    if not dados:
        return None
    if check_password_hash(dados["senha"], senha):
        return Usuario.de_dict(dados)
    return None


# ──────────────────────────────────────────
# Perfil
# ──────────────────────────────────────────

def buscar_usuario(login) -> Usuario | None:
    dados = banco.buscar_usuario(login)
    if not dados:
        return None
    usuario = Usuario.de_dict(dados)
    usuario.preparar_agua_do_dia()
    return usuario

def alterar_idioma(login, idioma):
    from services.i18n import normalize_language
    idioma = normalize_language(idioma)
    usuario = buscar_usuario(login)
    if not usuario:
        return False
    usuario.idioma = idioma
    banco.salvar_usuario(usuario.para_dict())
    return True


def atualizar_perfil(login, campos: dict):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    try:
        idade=int(campos.get("idade",usuario.idade)); altura=float(campos.get("altura",usuario.altura)); peso=float(campos.get("peso",usuario.peso)); meta=float(campos.get("meta_agua",usuario.meta_agua))
    except (TypeError,ValueError):
        return False, translate("profile.invalid_numbers")
    if not 0 <= idade <= 120: return False, translate("register.invalid_age")
    if not 0.5 <= altura <= 2.5: return False, translate("profile.invalid_height")
    if not 1 <= peso <= 500: return False, translate("register.invalid_weight")
    if not 0.5 <= meta <= 10: return False, translate("profile.invalid_water")
    usuario.nome=str(campos.get("nome",usuario.nome)).strip(); usuario.idade=idade; usuario.altura=altura; usuario.peso=peso; usuario.meta_agua=meta; usuario.tipo_sanguineo=str(campos.get("tipo_sanguineo",usuario.tipo_sanguineo)); usuario.observacoes=str(campos.get("observacoes",usuario.observacoes)).strip()
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.sync_profile(login, usuario)
    return True, translate("profile.updated")


def deletar_conta(login):
    return banco.deletar_usuario(login)


def alterar_senha(login, senha_atual, nova_senha):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    if not check_password_hash(usuario.senha, senha_atual):
        return False, translate("settings.current_password_invalid")
    if len(nova_senha or "") < 8:
        return False, translate("settings.password_short")
    usuario.senha = generate_password_hash(nova_senha)
    banco.salvar_usuario(usuario.para_dict())
    return True, translate("settings.password_changed")


# ──────────────────────────────────────────
# Hidratação
# ──────────────────────────────────────────

def adicionar_agua(login, quantidade: float):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")

    try:
        quantidade = float(quantidade)
    except (ValueError, TypeError):
        return False, translate("dash.water_invalid")

    if quantidade <= 0:
        return False, translate("dash.water_positive")
    if quantidade > 2:
        return False, translate("dash.water_max_add")
    if usuario.agua_consumida + quantidade > 10:
        return False, translate("dash.water_daily_limit")

    usuario.adicionar_agua(quantidade)
    from utils.tempo import hoje
    usuario.agua_logs.append({"data": hoje(), "quantidade": quantidade})
    banco.salvar_usuario(usuario.para_dict())
    # O log é gravado separadamente para não depender da reescrita do usuário.
    data_registro = hoje()
    banco.registrar_agua_log(login, quantidade, data_registro)
    from services import gamificacao
    gamificacao.register_action(login, "agua_adicao", f"agua:{data_registro}:{len(usuario.agua_logs)}")
    if usuario.progresso_agua() >= 100:
        gamificacao.register_action(login, "meta_agua", f"meta_agua:{data_registro}")
    return True, translate("dash.water_added")


def resetar_agua(login):
    usuario = buscar_usuario(login)
    if not usuario:
        return False
    usuario.resetar_agua()
    banco.salvar_usuario(usuario.para_dict())
    return True


# ──────────────────────────────────────────
# Registros de saúde
# ──────────────────────────────────────────

def registrar_peso(login, valor: float):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return False, translate("dash.weight_invalid")
    if not 1 <= valor <= 500:
        return False, translate("register.invalid_weight")
    usuario.registrar_peso(valor)
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "registro_peso")
    return True, translate("dash.weight_saved")


def registrar_pressao(login, sistolica: int, diastolica: int):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    try:
        sistolica = int(sistolica)
        diastolica = int(diastolica)
    except (ValueError, TypeError):
        return False, translate("dash.pressure_invalid")
    if not 50 <= sistolica <= 300:
        return False, translate("dash.systolic_range")
    if not 30 <= diastolica <= 200:
        return False, translate("dash.diastolic_range")
    if diastolica >= sistolica:
        return False, translate("dash.diastolic_less")
    usuario.registrar_pressao(sistolica, diastolica)
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "registro_pressao")
    return True, translate("dash.pressure_saved")


def registrar_glicemia(login, valor: float):
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return False, translate("dash.glucose_invalid")
    if valor < 20 or valor > 1000:
        return False, translate("dash.glucose_range")
    usuario.registrar_glicemia(valor)
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "registro_glicemia")
    return True, translate("dash.glucose_saved")


# ──────────────────────────────────────────
# Consultas
# ──────────────────────────────────────────

def adicionar_consulta(login, dados: dict):
    from models.consulta import Consulta
    from datetime import date
    usuario = buscar_usuario(login)
    if not usuario:
        return False, translate("common.user_not_found")
    medico = dados.get("medico", "").strip()
    especialidade = dados.get("especialidade", "").strip()
    if len(medico) < 2 or len(especialidade) < 2:
        return False, translate("consultations.invalid_fields")
    data = dados.get("data") or str(date.today())
    try:
        date.fromisoformat(data)
    except ValueError:
        return False, translate("consultations.invalid_date")
    consulta = Consulta(medico=medico, crm=dados.get("crm", "").strip(),
                        especialidade=especialidade, diagnostico=dados.get("diagnostico", "").strip(),
                        observacoes=dados.get("observacoes", "").strip(), data=data)
    usuario.consultas.append(consulta.para_dict())
    banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "consulta", f"consulta:{consulta.id}")
    return True, translate("consultations.added_success")


def remover_consulta(login, consulta_id: str):
    usuario = buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    antes=len(usuario.consultas)
    usuario.consultas=[c for c in usuario.consultas if c["id"] != consulta_id]
    if len(usuario.consultas)==antes: return False, translate("consultations.not_found")
    banco.salvar_usuario(usuario.para_dict()); return True, translate("consultations.removed_success")


# ──────────────────────────────────────────
# Receitas
# ──────────────────────────────────────────

def adicionar_receita(login, medico, crm, medicamentos: list[dict]):
    from models.receita import Receita, Medicamento
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    medico=medico.strip()
    medicamentos=[m for m in medicamentos if m.get("nome","").strip()]
    if len(medico)<2: return False, translate("prescriptions.doctor_required")
    if not medicamentos: return False, translate("prescriptions.medication_required")
    if len(medicamentos)>20: return False, translate("prescriptions.medication_limit")
    receita=Receita(medico=medico,crm=crm.strip())
    for m in medicamentos:
        nome=m.get("nome","").strip()
        if len(nome)<2: continue
        receita.adicionar_medicamento(Medicamento(nome=nome,dosagem=m.get("dosagem","").strip(),frequencia=m.get("frequencia","").strip(),duracao=m.get("duracao","").strip()))
    usuario.receitas.append(receita.para_dict()); banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "receita", f"receita:{receita.id}")
    return True, translate("prescriptions.added_success")


def remover_receita(login, receita_id: str):
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    antes=len(usuario.receitas); usuario.receitas=[r for r in usuario.receitas if r["id"]!=receita_id]
    if len(usuario.receitas)==antes: return False, translate("prescriptions.not_found")
    banco.salvar_usuario(usuario.para_dict()); return True, translate("prescriptions.removed_success")


# ──────────────────────────────────────────
# Exames
# ──────────────────────────────────────────

def adicionar_exame(login, tipo, resultado, observacoes, arquivo=None):
    from models.exame import Exame
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    tipo=tipo.strip()
    if len(tipo)<2: return False, translate("exams.type_required")
    if len(tipo)>120: return False, translate("exams.type_too_long")
    exame=Exame(tipo=tipo,resultado=resultado.strip(),observacoes=observacoes.strip(),arquivo=arquivo)
    usuario.exames.append(exame.para_dict()); banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "exame", f"exame:{exame.id}")
    return True, translate("exams.added_success")


def remover_exame(login, exame_id: str):
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    antes=len(usuario.exames); usuario.exames=[e for e in usuario.exames if e["id"]!=exame_id]
    if len(usuario.exames)==antes: return False, translate("exams.not_found")
    banco.salvar_usuario(usuario.para_dict()); return True, translate("exams.removed_success")


# ──────────────────────────────────────────
# Agendamentos
# ──────────────────────────────────────────

def criar_agendamento(login, dados: dict):
    from models.agendamento import Agendamento
    from datetime import date, datetime
    from zoneinfo import ZoneInfo
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    medico=dados.get("medico","").strip(); especialidade=dados.get("especialidade","").strip(); data=dados.get("data_consulta",""); hora=dados.get("hora","")
    if len(medico)<2 or len(especialidade)<2: return False, translate("consultations.invalid_fields")
    try:
        dt=datetime.strptime(f"{data} {hora}","%Y-%m-%d %H:%M")
    except ValueError: return False, translate("appointments.datetime_invalid")
    if dt <= datetime.now(ZoneInfo("America/Sao_Paulo")).replace(tzinfo=None): return False, translate("appointments.future_server")
    if any(a["status"]=="agendado" and a["data_consulta"]==data and a["hora"]==hora for a in usuario.agendamentos):
        return False, translate("appointments.duplicate")
    a=Agendamento(medico=medico,crm=dados.get("crm","").strip(),especialidade=especialidade,data_consulta=data,hora=hora,local=dados.get("local","").strip(),observacoes=dados.get("observacoes","").strip())
    usuario.agendamentos.append(a.para_dict()); banco.salvar_usuario(usuario.para_dict())
    from services import gamificacao
    gamificacao.register_action(login, "agendamento", f"agendamento:{a.id}")
    return True, translate("appointments.added_success")


def cancelar_agendamento(login, agendamento_id: str):
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    alvo=next((a for a in usuario.agendamentos if a["id"]==agendamento_id),None)
    if not alvo: return False, translate("appointments.not_found")
    if alvo["status"]!="agendado": return False, translate("appointments.cannot_cancel")
    alvo["status"]="cancelado"; banco.salvar_usuario(usuario.para_dict()); return True, translate("appointments.cancelled")


def concluir_agendamento(login, agendamento_id: str, diagnostico="", observacoes=""):
    usuario=buscar_usuario(login)
    if not usuario: return False, translate("common.user_not_found")
    alvo=next((a for a in usuario.agendamentos if a["id"]==agendamento_id),None)
    if not alvo: return False, translate("appointments.not_found")
    if alvo["status"]!="agendado": return False, translate("appointments.already_completed")
    alvo["status"]="realizado"
    from models.consulta import Consulta
    consulta=Consulta(medico=alvo["medico"],crm=alvo.get("crm",""),especialidade=alvo["especialidade"],diagnostico=diagnostico.strip(),observacoes=observacoes.strip() or alvo.get("observacoes",""),data=alvo["data_consulta"])
    usuario.consultas.append(consulta.para_dict()); banco.salvar_usuario(usuario.para_dict())
    return True, translate("appointments.completed_success")


# ──────────────────────────────────────────
# Prontuário eletrônico
# ──────────────────────────────────────────

def atualizar_prontuario(login, alergias=None, doencas_cronicas=None,
                          medicamentos_continuos=None):
    usuario = buscar_usuario(login)
    if not usuario:
        return False
    if alergias is not None:
        usuario.alergias = alergias
    if doencas_cronicas is not None:
        usuario.doencas_cronicas = doencas_cronicas
    if medicamentos_continuos is not None:
        usuario.medicamentos_continuos = medicamentos_continuos
    banco.salvar_usuario(usuario.para_dict())
    return True
