from datetime import date
from utils.tempo import hoje


class Usuario:
    """
    Modelo principal do sistema. Encapsula todos os dados de saúde do usuário
    e fornece métodos de cálculo e transformação.
    Preparado para futura migração: cada atributo mapeará diretamente para uma coluna SQL.
    """

    def __init__(self, login, senha, nome="", idade=0, altura=0.0,
                 peso=0.0, tipo_sanguineo="", observacoes="",
                 agua_consumida=0.0, meta_agua=2.0,
                 historico_peso=None, historico_pressao=None,
                 historico_glicemia=None, consultas=None,
                 receitas=None, exames=None, agendamentos=None,
                 alergias=None, doencas_cronicas=None,
                 medicamentos_continuos=None, foto_perfil=None, idioma='pt-BR', agua_data='', agua_logs=None):

        # Identificação
        self.login = login
        self.senha = senha
        self.nome = nome
        self.idade = idade
        self.foto_perfil = foto_perfil
        self.idioma = idioma or 'pt-BR'
        self.agua_data = agua_data or hoje()
        self.agua_logs = agua_logs or []

        # Medidas corporais
        self.altura = altura          # metros
        self.peso = peso              # kg
        self.tipo_sanguineo = tipo_sanguineo
        self.observacoes = observacoes

        # Hidratação
        self.agua_consumida = agua_consumida   # litros
        self.meta_agua = meta_agua             # litros

        # Históricos (listas de dicts)
        self.historico_peso = historico_peso or []
        self.historico_pressao = historico_pressao or []
        self.historico_glicemia = historico_glicemia or []

        # Registros médicos (listas de dicts)
        self.consultas = consultas or []
        self.receitas = receitas or []
        self.exames = exames or []
        self.agendamentos = agendamentos or []

        # Prontuário eletrônico — informações clínicas persistentes
        self.alergias = alergias or []                       # lista de strings
        self.doencas_cronicas = doencas_cronicas or []        # lista de strings
        self.medicamentos_continuos = medicamentos_continuos or []  # lista de strings

    # ──────────────────────────────────────────
    # IMC
    # ──────────────────────────────────────────
    def calcular_imc(self):
        if self.altura and self.altura > 0:
            return round(self.peso / (self.altura ** 2), 2)
        return 0.0

    def classificar_imc(self):
        imc = self.calcular_imc()
        if imc == 0:
            return "Sem dados"
        if imc < 18.5:
            return "Abaixo do peso"
        if imc < 25:
            return "Peso normal"
        if imc < 30:
            return "Sobrepeso"
        if imc < 35:
            return "Obesidade grau I"
        if imc < 40:
            return "Obesidade grau II"
        return "Obesidade grau III"

    # ──────────────────────────────────────────
    # Validações
    # ──────────────────────────────────────────
    def eh_maior_de_idade(self):
        return self.idade >= 18

    # ──────────────────────────────────────────
    # Hidratação
    # ──────────────────────────────────────────
    def preparar_agua_do_dia(self):
        data_atual = hoje()
        if self.agua_data != data_atual:
            self.agua_data = data_atual
            self.agua_consumida = 0.0

    def adicionar_agua(self, quantidade):
        self.preparar_agua_do_dia()
        if quantidade <= 0 or quantidade > 2:
            return False
        if self.agua_consumida + quantidade > 10:
            return False
        self.agua_consumida += quantidade
        return True

    def progresso_agua(self):
        self.preparar_agua_do_dia()
        if self.meta_agua and self.meta_agua > 0:
            return round((self.agua_consumida / self.meta_agua) * 100, 1)
        return 0.0

    def resetar_agua(self):
        self.agua_consumida = 0.0
        self.agua_data = hoje()

    # ──────────────────────────────────────────
    # Histórico de peso
    # ──────────────────────────────────────────
    def registrar_peso(self, valor):
        if valor < 1 or valor > 500:
            return False
        self.peso = valor
        self.historico_peso.append({
            "data": hoje(),
            "valor": valor
        })
        return True

    # ──────────────────────────────────────────
    # Histórico de pressão
    # ──────────────────────────────────────────
    def registrar_pressao(self, sistolica, diastolica):
        if not 50 <= sistolica <= 300 or not 30 <= diastolica <= 200:
            return False
        if diastolica >= sistolica:
            return False
        self.historico_pressao.append({
            "data": hoje(),
            "sistolica": sistolica,
            "diastolica": diastolica
        })
        return True

    def ultima_pressao(self):
        if self.historico_pressao:
            return self.historico_pressao[-1]
        return None

    def media_pressao_30dias(self):
        from datetime import timedelta
        corte = date.today() - timedelta(days=30)
        recentes = [p for p in self.historico_pressao
                    if date.fromisoformat(p["data"]) >= corte]
        if not recentes:
            return None
        sis = round(sum(p["sistolica"] for p in recentes) / len(recentes), 1)
        dia = round(sum(p["diastolica"] for p in recentes) / len(recentes), 1)
        return {"sistolica": sis, "diastolica": dia, "n": len(recentes)}

    # ──────────────────────────────────────────
    # Histórico de glicemia
    # ──────────────────────────────────────────
    def registrar_glicemia(self, valor):
        if valor < 20 or valor > 1000:
            return False
        self.historico_glicemia.append({
            "data": hoje(),
            "valor": valor
        })
        return True

    def ultima_glicemia(self):
        if self.historico_glicemia:
            return self.historico_glicemia[-1]
        return None

    # ──────────────────────────────────────────
    # Alertas automáticos
    # ──────────────────────────────────────────
    def gerar_alertas(self):
        alertas = []

        # Pressão alta
        ultima = self.ultima_pressao()
        if ultima:
            if ultima["sistolica"] >= 140 or ultima["diastolica"] >= 90:
                alertas.append({
                    "tipo": "danger",
                    "chave": "dash.pressure_alert",
                    "valor": f"{ultima['sistolica']}/{ultima['diastolica']} mmHg",
                    "mensagem": f"⚠️ Pressão arterial elevada: {ultima['sistolica']}/{ultima['diastolica']} mmHg"
                })

        # Glicemia elevada
        glic = self.ultima_glicemia()
        if glic and glic["valor"] > 126:
            alertas.append({
                "tipo": "danger",
                "chave": "dash.glucose_alert",
                "valor": f"{glic['valor']} mg/dL",
                "mensagem": f"🩸 Glicemia elevada: {glic['valor']} mg/dL"
            })

        # Meta de água
        if self.progresso_agua() < 50:
            alertas.append({
                "tipo": "warning",
                "chave": "dash.hydration_alert",
                "valor": self.progresso_agua(),
                "mensagem": f"💧 Você atingiu apenas {self.progresso_agua()}% da meta de hidratação."
            })

        # IMC
        imc = self.calcular_imc()
        if imc and imc > 30:
            alertas.append({
                "tipo": "warning",
                "chave": "dash.bmi_alert",
                "valor": imc,
                "mensagem": f"⚖️ IMC de {imc} indica obesidade. Consulte um médico."
            })

        return alertas

    # ──────────────────────────────────────────
    # Prontuário eletrônico — timeline unificada
    # ──────────────────────────────────────────
    def gerar_prontuario(self):
        """
        Consolida consultas, exames e receitas em uma única linha do tempo,
        ordenada da mais recente para a mais antiga.
        """
        eventos = []
        for c in self.consultas:
            eventos.append({
                "tipo": "consulta", "data": c["data"],
                "titulo": f"Consulta — {c['especialidade']}",
                "detalhe": f"Dr(a). {c['medico']} (CRM {c.get('crm','—')})",
                "extra": c.get("diagnostico", ""),
                "ref": c,
            })
        for e in self.exames:
            eventos.append({
                "tipo": "exame", "data": e["data"],
                "titulo": f"Exame — {e['tipo']}",
                "detalhe": e.get("resultado", ""),
                "extra": e.get("observacoes", ""),
                "ref": e,
            })
        for r in self.receitas:
            meds = ", ".join(m["nome"] for m in r.get("medicamentos", []))
            eventos.append({
                "tipo": "receita", "data": r["data"],
                "titulo": "Receita médica",
                "detalhe": f"Dr(a). {r['medico']} — {meds}",
                "extra": "",
                "ref": r,
            })
        eventos.sort(key=lambda x: x["data"], reverse=True)
        return eventos

    # ──────────────────────────────────────────
    # Agendamentos
    # ──────────────────────────────────────────
    def agendamentos_futuros(self):
        from datetime import datetime
        from utils.tempo import agora
        futuros = []
        agora_local = agora().replace(tzinfo=None)
        for a in self.agendamentos:
            if a.get("status") != "agendado":
                continue
            try:
                dt = datetime.strptime(
                    f"{a.get('data_consulta','')} {a.get('hora','00:00')}",
                    "%Y-%m-%d %H:%M"
                )
                if dt > agora_local:
                    futuros.append(a)
            except ValueError:
                continue
        return futuros

    def agendamentos_passados(self):
        return [a for a in self.agendamentos if a["status"] != "agendado"]

    # ──────────────────────────────────────────
    # Serialização / Desserialização
    # ──────────────────────────────────────────
    def para_dict(self):
        return {
            "login": self.login,
            "senha": self.senha,
            "nome": self.nome,
            "foto_perfil": self.foto_perfil,
            "idioma": self.idioma,
            "agua_data": self.agua_data,
            "idade": self.idade,
            "altura": self.altura,
            "peso": self.peso,
            "tipo_sanguineo": self.tipo_sanguineo,
            "observacoes": self.observacoes,
            "agua_consumida": self.agua_consumida,
            "agua_logs": self.agua_logs,
            "meta_agua": self.meta_agua,
            "historico_peso": self.historico_peso,
            "historico_pressao": self.historico_pressao,
            "historico_glicemia": self.historico_glicemia,
            "consultas": self.consultas,
            "receitas": self.receitas,
            "exames": self.exames,
            "agendamentos": self.agendamentos,
            "alergias": self.alergias,
            "doencas_cronicas": self.doencas_cronicas,
            "medicamentos_continuos": self.medicamentos_continuos,
        }

    @classmethod
    def de_dict(cls, dados):
        return cls(
            login=dados.get("login"),
            senha=dados.get("senha"),
            nome=dados.get("nome", ""),
            foto_perfil=dados.get("foto_perfil"),
            idioma=dados.get("idioma", "pt-BR"),
            agua_data=dados.get("agua_data", hoje()),
            idade=dados.get("idade", 0),
            altura=dados.get("altura", 0.0),
            peso=dados.get("peso", 0.0),
            tipo_sanguineo=dados.get("tipo_sanguineo", ""),
            observacoes=dados.get("observacoes", ""),
            agua_consumida=dados.get("agua_consumida", 0.0),
            agua_logs=dados.get("agua_logs", []),
            meta_agua=dados.get("meta_agua", 2.0),
            historico_peso=dados.get("historico_peso", []),
            historico_pressao=dados.get("historico_pressao", []),
            historico_glicemia=dados.get("historico_glicemia", []),
            consultas=dados.get("consultas", []),
            receitas=dados.get("receitas", []),
            exames=dados.get("exames", []),
            agendamentos=dados.get("agendamentos", []),
            alergias=dados.get("alergias", []),
            doencas_cronicas=dados.get("doencas_cronicas", []),
            medicamentos_continuos=dados.get("medicamentos_continuos", []),
        )
