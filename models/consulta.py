"""
Modelo de Consulta Médica.
Encapsula os dados de uma consulta e oferece serialização bidirecional.
Cada consulta pertence a um usuário e é armazenada dentro do campo 'consultas'
no JSON do usuário — sem necessidade de chave estrangeira nesta fase.
"""
import uuid
from datetime import date


class Consulta:
    def __init__(self, medico, especialidade, diagnostico="",
                 crm="", observacoes="", data=None, id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.data = data or str(date.today())
        self.medico = medico
        self.crm = crm
        self.especialidade = especialidade
        self.diagnostico = diagnostico
        self.observacoes = observacoes

    def para_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "medico": self.medico,
            "crm": self.crm,
            "especialidade": self.especialidade,
            "diagnostico": self.diagnostico,
            "observacoes": self.observacoes,
        }

    @classmethod
    def de_dict(cls, d):
        return cls(
            id=d.get("id"),
            data=d.get("data"),
            medico=d.get("medico", ""),
            crm=d.get("crm", ""),
            especialidade=d.get("especialidade", ""),
            diagnostico=d.get("diagnostico", ""),
            observacoes=d.get("observacoes", ""),
        )
