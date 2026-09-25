"""
Modelo de Agendamento de Consulta.
Representa um horário futuro marcado pelo paciente — diferente de Consulta,
que é o REGISTRO HISTÓRICO de uma consulta já realizada.

Fluxo: Agendamento (status=agendado) -> paciente marca como realizada
       -> vira um registro Consulta no prontuário -> Agendamento muda para status=realizado
       Ou o paciente pode cancelar -> status=cancelado
"""
import uuid
from datetime import date


class Agendamento:
    STATUS_VALIDOS = {"agendado", "realizado", "cancelado"}

    def __init__(self, medico, especialidade, data_consulta, hora,
                 crm="", local="", observacoes="", status="agendado", id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.medico = medico
        self.crm = crm
        self.especialidade = especialidade
        self.data_consulta = data_consulta   # data da consulta futura
        self.hora = hora
        self.local = local
        self.observacoes = observacoes
        self.status = status if status in self.STATUS_VALIDOS else "agendado"
        self.criado_em = str(date.today())

    def esta_atrasado(self):
        """Indica se a data já passou e o agendamento ainda está como 'agendado'."""
        try:
            return self.status == "agendado" and date.fromisoformat(self.data_consulta) < date.today()
        except ValueError:
            return False

    def para_dict(self):
        return {
            "id": self.id,
            "medico": self.medico,
            "crm": self.crm,
            "especialidade": self.especialidade,
            "data_consulta": self.data_consulta,
            "hora": self.hora,
            "local": self.local,
            "observacoes": self.observacoes,
            "status": self.status,
            "criado_em": self.criado_em,
        }

    @classmethod
    def de_dict(cls, d):
        obj = cls(
            id=d.get("id"),
            medico=d.get("medico", ""),
            crm=d.get("crm", ""),
            especialidade=d.get("especialidade", ""),
            data_consulta=d.get("data_consulta", ""),
            hora=d.get("hora", ""),
            local=d.get("local", ""),
            observacoes=d.get("observacoes", ""),
            status=d.get("status", "agendado"),
        )
        obj.criado_em = d.get("criado_em", obj.criado_em)
        return obj
