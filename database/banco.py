"""Persistência SQLite do SaúdeApp 2.0.

A camada mantém uma API simples para os Services, mas os dados ficam em
um banco relacional (.db), com tabelas para os principais registros.
"""
from __future__ import annotations
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DB = os.path.join(BASE_DIR, "database", "saudeapp.db")
CAMINHO_JSON = os.path.join(BASE_DIR, "data", "usuarios_backup.json")


def _conexao():
    os.makedirs(os.path.dirname(CAMINHO_DB), exist_ok=True)
    conn = sqlite3.connect(CAMINHO_DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def _db():
    conn = _conexao()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def inicializar():
    with _db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            login TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL DEFAULT '',
            idade INTEGER NOT NULL DEFAULT 0,
            altura REAL NOT NULL DEFAULT 0,
            peso REAL NOT NULL DEFAULT 0,
            tipo_sanguineo TEXT NOT NULL DEFAULT '',
            observacoes TEXT NOT NULL DEFAULT '',
            agua_consumida REAL NOT NULL DEFAULT 0,
            meta_agua REAL NOT NULL DEFAULT 2,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            foto_perfil TEXT,
            idioma TEXT NOT NULL DEFAULT 'pt-BR',
            agua_data TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS historico_peso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            valor REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS historico_pressao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            sistolica INTEGER NOT NULL,
            diastolica INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS historico_glicemia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            valor REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS agua_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            quantidade REAL NOT NULL,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS consultas (
            id TEXT PRIMARY KEY,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            medico TEXT NOT NULL,
            crm TEXT NOT NULL DEFAULT '',
            especialidade TEXT NOT NULL,
            diagnostico TEXT NOT NULL DEFAULT '',
            observacoes TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS receitas (
            id TEXT PRIMARY KEY,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            medico TEXT NOT NULL,
            crm TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS medicamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receita_id TEXT NOT NULL REFERENCES receitas(id) ON DELETE CASCADE,
            nome TEXT NOT NULL,
            dosagem TEXT NOT NULL DEFAULT '',
            frequencia TEXT NOT NULL DEFAULT '',
            duracao TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS exames (
            id TEXT PRIMARY KEY,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            resultado TEXT NOT NULL DEFAULT '',
            observacoes TEXT NOT NULL DEFAULT '',
            arquivo TEXT
        );
        CREATE TABLE IF NOT EXISTS agendamentos (
            id TEXT PRIMARY KEY,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            medico TEXT NOT NULL,
            crm TEXT NOT NULL DEFAULT '',
            especialidade TEXT NOT NULL,
            data_consulta TEXT NOT NULL,
            hora TEXT NOT NULL,
            local TEXT NOT NULL DEFAULT '',
            observacoes TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'agendado',
            criado_em TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS prontuario (
            usuario_login TEXT PRIMARY KEY REFERENCES usuarios(login) ON DELETE CASCADE,
            alergias TEXT NOT NULL DEFAULT '[]',
            doencas_cronicas TEXT NOT NULL DEFAULT '[]',
            medicamentos_continuos TEXT NOT NULL DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS documentos (
            token TEXT PRIMARY KEY,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            tipo TEXT NOT NULL,
            referencia_id TEXT,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            chave TEXT NOT NULL,
            titulo TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'info',
            lida INTEGER NOT NULL DEFAULT 0,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(usuario_login, chave)
        );
        CREATE TABLE IF NOT EXISTS gamificacao (
            usuario_login TEXT PRIMARY KEY REFERENCES usuarios(login) ON DELETE CASCADE,
            xp INTEGER NOT NULL DEFAULT 0,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS gamificacao_eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            chave TEXT NOT NULL,
            tipo TEXT NOT NULL,
            xp INTEGER NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL DEFAULT '',
            UNIQUE(usuario_login, chave)
        );
        CREATE TABLE IF NOT EXISTS gamificacao_conquistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_login TEXT NOT NULL REFERENCES usuarios(login) ON DELETE CASCADE,
            codigo TEXT NOT NULL,
            desbloqueada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(usuario_login, codigo)
        );
        CREATE INDEX IF NOT EXISTS idx_game_eventos_usuario_data ON gamificacao_eventos(usuario_login, data);

        CREATE INDEX IF NOT EXISTS idx_peso_usuario_data ON historico_peso(usuario_login, data);
        CREATE INDEX IF NOT EXISTS idx_pressao_usuario_data ON historico_pressao(usuario_login, data);
        CREATE INDEX IF NOT EXISTS idx_glic_usuario_data ON historico_glicemia(usuario_login, data);
        CREATE INDEX IF NOT EXISTS idx_consultas_usuario_data ON consultas(usuario_login, data);
        CREATE INDEX IF NOT EXISTS idx_exames_usuario_data ON exames(usuario_login, data);
        CREATE INDEX IF NOT EXISTS idx_agend_usuario_data ON agendamentos(usuario_login, data_consulta, hora);
        CREATE INDEX IF NOT EXISTS idx_notif_usuario ON notificacoes(usuario_login, lida, criado_em);
        CREATE INDEX IF NOT EXISTS idx_agua_usuario_data ON agua_logs(usuario_login, data);
        """)

        # Migração simples para bancos .db criados antes do recurso de foto.
        colunas = {row[1] for row in db.execute("PRAGMA table_info(usuarios)").fetchall()}
        if "foto_perfil" not in colunas:
            db.execute("ALTER TABLE usuarios ADD COLUMN foto_perfil TEXT")
        if "idioma" not in colunas:
            db.execute("ALTER TABLE usuarios ADD COLUMN idioma TEXT NOT NULL DEFAULT 'pt-BR'")
        if "agua_data" not in colunas:
            db.execute("ALTER TABLE usuarios ADD COLUMN agua_data TEXT NOT NULL DEFAULT ''")


def _migrar_json_se_necessario():
    inicializar()
    with _db() as db:
        qtd = db.execute("SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"]
    if qtd or not os.path.exists(CAMINHO_JSON):
        return False

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    with _db() as db:
        for u in dados.values():
            db.execute("""INSERT OR IGNORE INTO usuarios
                (login, senha, nome, idade, altura, peso, tipo_sanguineo, observacoes,
                 agua_consumida, meta_agua) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (u.get("login", ""), u.get("senha", ""), u.get("nome", ""),
                 u.get("idade", 0), u.get("altura", 0), u.get("peso", 0),
                 u.get("tipo_sanguineo", ""), u.get("observacoes", ""),
                 u.get("agua_consumida", 0), u.get("meta_agua", 2)))
            login = u.get("login", "")
            for p in u.get("historico_peso", []):
                db.execute("INSERT INTO historico_peso(usuario_login,data,valor) VALUES(?,?,?)", (login,p.get("data",str(date.today())),p.get("valor",0)))
            for p in u.get("historico_pressao", []):
                db.execute("INSERT INTO historico_pressao(usuario_login,data,sistolica,diastolica) VALUES(?,?,?,?)", (login,p.get("data",str(date.today())),p.get("sistolica",0),p.get("diastolica",0)))
            for g in u.get("historico_glicemia", []):
                db.execute("INSERT INTO historico_glicemia(usuario_login,data,valor) VALUES(?,?,?)", (login,g.get("data",str(date.today())),g.get("valor",0)))
            db.execute("INSERT OR REPLACE INTO prontuario(usuario_login,alergias,doencas_cronicas,medicamentos_continuos) VALUES(?,?,?,?)",
                       (login,json.dumps(u.get("alergias",[]),ensure_ascii=False),json.dumps(u.get("doencas_cronicas",[]),ensure_ascii=False),json.dumps(u.get("medicamentos_continuos",[]),ensure_ascii=False)))
            for c in u.get("consultas", []):
                db.execute("INSERT OR IGNORE INTO consultas VALUES(?,?,?,?,?,?,?,?)", (c.get("id"),login,c.get("data",str(date.today())),c.get("medico",""),c.get("crm",""),c.get("especialidade",""),c.get("diagnostico",""),c.get("observacoes","")))
            for r in u.get("receitas", []):
                db.execute("INSERT OR IGNORE INTO receitas VALUES(?,?,?,?,?)", (r.get("id"),login,r.get("data",str(date.today())),r.get("medico",""),r.get("crm","")))
                for m in r.get("medicamentos", []):
                    db.execute("INSERT INTO medicamentos(receita_id,nome,dosagem,frequencia,duracao) VALUES(?,?,?,?,?)", (r.get("id"),m.get("nome",""),m.get("dosagem",""),m.get("frequencia",""),m.get("duracao","")))
            for e in u.get("exames", []):
                db.execute("INSERT OR IGNORE INTO exames VALUES(?,?,?,?,?, ?,?)", (e.get("id"),login,e.get("data",str(date.today())),e.get("tipo",""),e.get("resultado",""),e.get("observacoes",""),e.get("arquivo")))
            for a in u.get("agendamentos", []):
                db.execute("INSERT OR IGNORE INTO agendamentos VALUES(?,?,?,?,?,?,?,?,?,?,?)", (a.get("id"),login,a.get("medico",""),a.get("crm",""),a.get("especialidade",""),a.get("data_consulta",""),a.get("hora",""),a.get("local",""),a.get("observacoes",""),a.get("status","agendado"),a.get("criado_em",str(date.today()))))
    return True


def inicializar_e_migrar():
    return _migrar_json_se_necessario()


def buscar_usuario(login: str):
    inicializar()
    with _db() as db:
        u = db.execute("SELECT * FROM usuarios WHERE login=?", (login,)).fetchone()
        if not u:
            return None
        d = dict(u)
        d.pop("criado_em", None); d.pop("atualizado_em", None)
        d["idioma"] = d.get("idioma") or "pt-BR"
        d["agua_data"] = d.get("agua_data") or str(date.today())
        d["historico_peso"] = [dict(x) | {"valor": x["valor"]} for x in db.execute("SELECT data,valor FROM historico_peso WHERE usuario_login=? ORDER BY id",(login,))]
        d["historico_pressao"] = [dict(x) for x in db.execute("SELECT data,sistolica,diastolica FROM historico_pressao WHERE usuario_login=? ORDER BY id",(login,))]
        d["historico_glicemia"] = [dict(x) for x in db.execute("SELECT data,valor FROM historico_glicemia WHERE usuario_login=? ORDER BY id",(login,))]
        d["agua_logs"] = [dict(x) for x in db.execute("SELECT data,quantidade,criado_em FROM agua_logs WHERE usuario_login=? ORDER BY id", (login,))]
        d["consultas"] = [dict(x) for x in db.execute("SELECT id,data,medico,crm,especialidade,diagnostico,observacoes FROM consultas WHERE usuario_login=? ORDER BY data DESC",(login,))]
        d["receitas"] = []
        for r in db.execute("SELECT id,data,medico,crm FROM receitas WHERE usuario_login=? ORDER BY data DESC",(login,)):
            rd=dict(r); rd["medicamentos"]=[dict(x) for x in db.execute("SELECT nome,dosagem,frequencia,duracao FROM medicamentos WHERE receita_id=? ORDER BY id",(r["id"],))]; d["receitas"].append(rd)
        d["exames"] = [dict(x) for x in db.execute("SELECT id,data,tipo,resultado,observacoes,arquivo FROM exames WHERE usuario_login=? ORDER BY data DESC",(login,))]
        d["agendamentos"] = [dict(x) for x in db.execute("SELECT id,medico,crm,especialidade,data_consulta,hora,local,observacoes,status,criado_em FROM agendamentos WHERE usuario_login=? ORDER BY data_consulta,hora",(login,))]
        p=db.execute("SELECT * FROM prontuario WHERE usuario_login=?",(login,)).fetchone()
        d["alergias"]=json.loads(p["alergias"]) if p else []
        d["doencas_cronicas"]=json.loads(p["doencas_cronicas"]) if p else []
        d["medicamentos_continuos"]=json.loads(p["medicamentos_continuos"]) if p else []
        return d


def salvar_usuario(dados_usuario: dict):
    inicializar()
    login=dados_usuario["login"]
    with _db() as db:
        db.execute("""INSERT INTO usuarios(login,senha,nome,idade,altura,peso,tipo_sanguineo,observacoes,agua_consumida,meta_agua,foto_perfil,idioma,agua_data)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(login) DO UPDATE SET senha=excluded.senha,nome=excluded.nome,
            idade=excluded.idade,altura=excluded.altura,peso=excluded.peso,tipo_sanguineo=excluded.tipo_sanguineo,
            observacoes=excluded.observacoes,agua_consumida=excluded.agua_consumida,meta_agua=excluded.meta_agua,
            foto_perfil=excluded.foto_perfil, idioma=excluded.idioma,
            agua_data=excluded.agua_data, atualizado_em=CURRENT_TIMESTAMP""",
            (login,dados_usuario.get("senha",""),dados_usuario.get("nome",""),dados_usuario.get("idade",0),dados_usuario.get("altura",0),dados_usuario.get("peso",0),dados_usuario.get("tipo_sanguineo",""),dados_usuario.get("observacoes",""),dados_usuario.get("agua_consumida",0),dados_usuario.get("meta_agua",2),dados_usuario.get("foto_perfil"),
             dados_usuario.get("idioma","pt-BR"), dados_usuario.get("agua_data",str(date.today()))))
        # Compatibilidade: salvar_usuario continua aceitando o dict antigo inteiro.
        db.execute("DELETE FROM historico_peso WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO historico_peso(usuario_login,data,valor) VALUES(?,?,?)",[(login,p.get("data",str(date.today())),p.get("valor",0)) for p in dados_usuario.get("historico_peso",[])])
        db.execute("DELETE FROM historico_pressao WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO historico_pressao(usuario_login,data,sistolica,diastolica) VALUES(?,?,?,?)",[(login,p.get("data",str(date.today())),p.get("sistolica",0),p.get("diastolica",0)) for p in dados_usuario.get("historico_pressao",[])])
        db.execute("DELETE FROM historico_glicemia WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO historico_glicemia(usuario_login,data,valor) VALUES(?,?,?)",[(login,g.get("data",str(date.today())),g.get("valor",0)) for g in dados_usuario.get("historico_glicemia",[])])
        # Logs de hidratação são incrementais e não fazem parte do JSON legado.
        # Eles só são inseridos quando vierem explicitamente no dicionário.
        if "agua_logs" in dados_usuario:
            db.execute("DELETE FROM agua_logs WHERE usuario_login=?", (login,))
            db.executemany("INSERT INTO agua_logs(usuario_login,data,quantidade,criado_em) VALUES(?,?,?,?)", [(login, x.get("data", str(date.today())), x.get("quantidade", 0), x.get("criado_em", str(date.today()))) for x in dados_usuario.get("agua_logs", [])])
        db.execute("DELETE FROM consultas WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO consultas VALUES(?,?,?,?,?,?,?,?)",[(c.get("id"),login,c.get("data",str(date.today())),c.get("medico",""),c.get("crm",""),c.get("especialidade",""),c.get("diagnostico",""),c.get("observacoes","")) for c in dados_usuario.get("consultas",[])])
        db.execute("DELETE FROM receitas WHERE usuario_login=?",(login,)); db.execute("DELETE FROM medicamentos WHERE receita_id NOT IN (SELECT id FROM receitas)")
        for r in dados_usuario.get("receitas",[]):
            db.execute("INSERT INTO receitas VALUES(?,?,?,?,?)",(r.get("id"),login,r.get("data",str(date.today())),r.get("medico",""),r.get("crm","")))
            db.executemany("INSERT INTO medicamentos(receita_id,nome,dosagem,frequencia,duracao) VALUES(?,?,?,?,?)",[(r.get("id"),m.get("nome",""),m.get("dosagem",""),m.get("frequencia",""),m.get("duracao","")) for m in r.get("medicamentos",[])])
        db.execute("DELETE FROM exames WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO exames VALUES(?,?,?,?,?,?,?)",[(e.get("id"),login,e.get("data",str(date.today())),e.get("tipo",""),e.get("resultado",""),e.get("observacoes",""),e.get("arquivo")) for e in dados_usuario.get("exames",[])])
        db.execute("DELETE FROM agendamentos WHERE usuario_login=?",(login,)); db.executemany("INSERT INTO agendamentos VALUES(?,?,?,?,?,?,?,?,?,?,?)",[(a.get("id"),login,a.get("medico",""),a.get("crm",""),a.get("especialidade",""),a.get("data_consulta",""),a.get("hora",""),a.get("local",""),a.get("observacoes",""),a.get("status","agendado"),a.get("criado_em",str(date.today()))) for a in dados_usuario.get("agendamentos",[])])
        db.execute("INSERT INTO prontuario(usuario_login,alergias,doencas_cronicas,medicamentos_continuos) VALUES(?,?,?,?) ON CONFLICT(usuario_login) DO UPDATE SET alergias=excluded.alergias,doencas_cronicas=excluded.doencas_cronicas,medicamentos_continuos=excluded.medicamentos_continuos",(login,json.dumps(dados_usuario.get("alergias",[]),ensure_ascii=False),json.dumps(dados_usuario.get("doencas_cronicas",[]),ensure_ascii=False),json.dumps(dados_usuario.get("medicamentos_continuos",[]),ensure_ascii=False)))


def deletar_usuario(login: str):
    inicializar()
    with _db() as db:
        cur=db.execute("DELETE FROM usuarios WHERE login=?",(login,))
        return cur.rowcount>0


def login_existe(login: str):
    inicializar()
    with _db() as db:
        return db.execute("SELECT 1 FROM usuarios WHERE login=?",(login,)).fetchone() is not None


def registrar_documento(token, login, tipo, referencia_id=None):
    with _db() as db:
        db.execute("INSERT INTO documentos(token,usuario_login,tipo,referencia_id) VALUES(?,?,?,?)",(token,login,tipo,referencia_id))


def buscar_documento(token):
    with _db() as db:
        row=db.execute("SELECT * FROM documentos WHERE token=?",(token,)).fetchone()
        return dict(row) if row else None


def registrar_agua_log(login, quantidade, data_registro):
    inicializar()
    with _db() as db:
        db.execute("INSERT INTO agua_logs(usuario_login,data,quantidade) VALUES(?,?,?)", (login, data_registro, quantidade))


def criar_notificacao(login, chave, titulo, mensagem, tipo="info"):
    inicializar()
    with _db() as db:
        db.execute("INSERT OR IGNORE INTO notificacoes(usuario_login,chave,titulo,mensagem,tipo) VALUES(?,?,?,?,?)", (login, chave, titulo, mensagem, tipo))


def listar_notificacoes(login, limite=30):
    inicializar()
    with _db() as db:
        return [dict(x) for x in db.execute("SELECT id,titulo,mensagem,tipo,lida,criado_em FROM notificacoes WHERE usuario_login=? ORDER BY lida ASC, id DESC LIMIT ?", (login, limite))]


def contar_nao_lidas(login):
    inicializar()
    with _db() as db:
        return db.execute("SELECT COUNT(*) AS n FROM notificacoes WHERE usuario_login=? AND lida=0", (login,)).fetchone()["n"]


def marcar_notificacao_lida(login, notification_id):
    inicializar()
    with _db() as db:
        db.execute("UPDATE notificacoes SET lida=1 WHERE id=? AND usuario_login=?", (notification_id, login))


def marcar_todas_lidas(login):
    inicializar()
    with _db() as db:
        db.execute("UPDATE notificacoes SET lida=1 WHERE usuario_login=?", (login,))
