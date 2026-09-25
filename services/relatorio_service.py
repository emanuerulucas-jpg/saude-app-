"""
Serviço de geração de relatório PDF usando ReportLab.
Gera um PDF completo com dados pessoais, sinais vitais, consultas, receitas e exames.
"""
import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from models.usuario import Usuario


AZUL = colors.HexColor("#2563eb")
CINZA = colors.HexColor("#6b7280")
CLARO = colors.HexColor("#eff6ff")


def gerar_pdf(usuario: Usuario) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("Titulo", parent=styles["Heading1"],
                                   textColor=AZUL, fontSize=20, spaceAfter=4)
    h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
                               textColor=AZUL, fontSize=13, spaceBefore=14, spaceAfter=4)
    normal = styles["Normal"]
    small = ParagraphStyle("Small", parent=normal, fontSize=9, textColor=CINZA)

    elementos = []

    # Cabeçalho
    elementos.append(Paragraph("📋 Relatório de Saúde", titulo_style))
    elementos.append(Paragraph(
        f"Gerado em {date.today().strftime('%d/%m/%Y')} — Sistema de Monitoramento de Saúde",
        small))
    elementos.append(HRFlowable(width="100%", thickness=1, color=AZUL))
    elementos.append(Spacer(1, 0.3*cm))

    # Dados pessoais
    elementos.append(Paragraph("Dados Pessoais", h2_style))
    dados_pessoais = [
        ["Nome", usuario.nome or "—"],
        ["Login", usuario.login],
        ["Idade", f"{usuario.idade} anos"],
        ["Tipo Sanguíneo", usuario.tipo_sanguineo or "—"],
        ["Altura", f"{usuario.altura} m"],
        ["Peso atual", f"{usuario.peso} kg"],
        ["IMC", f"{usuario.calcular_imc()} — {usuario.classificar_imc()}"],
        ["Observações", usuario.observacoes or "—"],
    ]
    elementos.append(_tabela_dois_col(dados_pessoais))

    # Hidratação
    elementos.append(Paragraph("Hidratação", h2_style))
    elementos.append(Paragraph(
        f"Consumo atual: {usuario.agua_consumida} L | Meta: {usuario.meta_agua} L | "
        f"Progresso: {usuario.progresso_agua()}%", normal))

    # Histórico de pressão
    if usuario.historico_pressao:
        elementos.append(Paragraph("Histórico de Pressão Arterial", h2_style))
        rows = [["Data", "Sistólica (mmHg)", "Diastólica (mmHg)"]]
        for p in reversed(usuario.historico_pressao[-10:]):
            rows.append([p["data"], str(p["sistolica"]), str(p["diastolica"])])
        elementos.append(_tabela_header(rows))

    # Histórico de glicemia
    if usuario.historico_glicemia:
        elementos.append(Paragraph("Histórico de Glicemia", h2_style))
        rows = [["Data", "Valor (mg/dL)"]]
        for g in reversed(usuario.historico_glicemia[-10:]):
            rows.append([g["data"], str(g["valor"])])
        elementos.append(_tabela_header(rows))

    # Histórico de peso
    if usuario.historico_peso:
        elementos.append(Paragraph("Histórico de Peso", h2_style))
        rows = [["Data", "Peso (kg)"]]
        for p in reversed(usuario.historico_peso[-10:]):
            rows.append([p["data"], str(p["valor"])])
        elementos.append(_tabela_header(rows))

    # Resumo clínico (alergias, doenças crônicas, medicamentos contínuos)
    if usuario.alergias or usuario.doencas_cronicas or usuario.medicamentos_continuos:
        elementos.append(Paragraph("Resumo Clínico", h2_style))
        if usuario.alergias:
            elementos.append(Paragraph(f"<b>Alergias:</b> {', '.join(usuario.alergias)}", normal))
        if usuario.doencas_cronicas:
            elementos.append(Paragraph(f"<b>Doenças crônicas:</b> {', '.join(usuario.doencas_cronicas)}", normal))
        if usuario.medicamentos_continuos:
            elementos.append(Paragraph(f"<b>Uso contínuo:</b> {', '.join(usuario.medicamentos_continuos)}", normal))

    # Próximos agendamentos
    futuros = usuario.agendamentos_futuros()
    if futuros:
        elementos.append(Paragraph("Próximas Consultas Agendadas", h2_style))
        rows = [["Data", "Hora", "Médico", "Especialidade", "Local"]]
        for a in sorted(futuros, key=lambda x: (x["data_consulta"], x["hora"])):
            rows.append([a["data_consulta"], a["hora"], a["medico"], a["especialidade"], a.get("local","—")])
        elementos.append(_tabela_header(rows))

    # Consultas
    if usuario.consultas:
        elementos.append(Paragraph("Consultas Médicas", h2_style))
        rows = [["Data", "Médico", "Especialidade", "Diagnóstico"]]
        for c in usuario.consultas:
            rows.append([c["data"], c["medico"], c["especialidade"], c.get("diagnostico","—")])
        elementos.append(_tabela_header(rows))

    # Receitas
    if usuario.receitas:
        elementos.append(Paragraph("Receitas Médicas", h2_style))
        for r in usuario.receitas:
            elementos.append(Paragraph(
                f"<b>{r['data']}</b> — Dr(a). {r['medico']} (CRM {r['crm']})", normal))
            for m in r.get("medicamentos", []):
                elementos.append(Paragraph(
                    f"  • {m['nome']} — {m['dosagem']} / {m['frequencia']} / {m['duracao']}",
                    normal))
            elementos.append(Spacer(1, 0.2*cm))

    # Exames
    if usuario.exames:
        elementos.append(Paragraph("Exames", h2_style))
        rows = [["Data", "Tipo", "Resultado", "Arquivo"]]
        for e in usuario.exames:
            rows.append([e["data"], e["tipo"], e.get("resultado","—"), e.get("arquivo","—")])
        elementos.append(_tabela_header(rows))

    doc.build(elementos)
    return buffer.getvalue()


# ── helpers ──────────────────────────────────────────────────────────

def _tabela_dois_col(dados):
    t = Table(dados, colWidths=[4.5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), CLARO),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, CLARO]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _tabela_header(rows):
    t = Table(rows, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CLARO]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t
