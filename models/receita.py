"""
Modelo de Receita Médica.
Cada receita contém uma lista de medicamentos com dosagem, frequência e duração.
A lista de medicamentos é tratada como Value Object — não tem ID próprio.
"""
import uuid
from datetime import date


class Medicamento:
    def __init__(self, nome, dosagem, frequencia, duracao):
        self.nome = nome
        self.dosagem = dosagem
        self.frequencia = frequencia
        self.duracao = duracao

    def para_dict(self):
        return {
            "nome": self.nome,
            "dosagem": self.dosagem,
            "frequencia": self.frequencia,
            "duracao": self.duracao,
        }

    @classmethod
    def de_dict(cls, d):
        return cls(
            nome=d.get("nome", ""),
            dosagem=d.get("dosagem", ""),
            frequencia=d.get("frequencia", ""),
            duracao=d.get("duracao", ""),
        )


class Receita:
    def __init__(self, medico, crm="", data=None, medicamentos=None, id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.data = data or str(date.today())
        self.medico = medico
        self.crm = crm
        self.medicamentos: list[Medicamento] = medicamentos or []

    def adicionar_medicamento(self, medicamento: Medicamento):
        self.medicamentos.append(medicamento)

    def para_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "medico": self.medico,
            "crm": self.crm,
            "medicamentos": [m.para_dict() for m in self.medicamentos],
        }

    @classmethod
    def de_dict(cls, d):
        meds = [Medicamento.de_dict(m) for m in d.get("medicamentos", [])]
        return cls(
            id=d.get("id"),
            data=d.get("data"),
            medico=d.get("medico", ""),
            crm=d.get("crm", ""),
            medicamentos=meds,
        )
