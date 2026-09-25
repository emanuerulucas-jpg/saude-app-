"""
Modelo de Exame Médico.
Suporta upload de arquivo (PDF/PNG/JPG) salvo em /uploads.
O campo 'arquivo' guarda apenas o nome do arquivo — o path completo é
construído dinamicamente no service para não vazar informações de diretório.
"""
import uuid
from datetime import date


class Exame:
    def __init__(self, tipo, resultado="", observacoes="",
                 arquivo=None, data=None, id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.data = data or str(date.today())
        self.tipo = tipo
        self.resultado = resultado
        self.observacoes = observacoes
        self.arquivo = arquivo   # nome do arquivo salvo, ex: "abc123_hemograma.pdf"

    def para_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "tipo": self.tipo,
            "resultado": self.resultado,
            "observacoes": self.observacoes,
            "arquivo": self.arquivo,
        }

    @classmethod
    def de_dict(cls, d):
        return cls(
            id=d.get("id"),
            data=d.get("data"),
            tipo=d.get("tipo", ""),
            resultado=d.get("resultado", ""),
            observacoes=d.get("observacoes", ""),
            arquivo=d.get("arquivo"),
        )
