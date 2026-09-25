"""Geração de documentos PDF claramente identificados como SIMULAÇÃO."""
from io import BytesIO
from datetime import datetime
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from database import banco
from services.i18n import translate
import secrets


def _pdf_base(titulo, subtitulo=""):
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=44,bottomMargin=44,title=titulo)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TituloSaude", parent=styles["Title"], fontSize=18, leading=22, textColor=colors.HexColor("#1d4ed8"), spaceAfter=6))
    styles.add(ParagraphStyle(name="Sub", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#64748b"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="Water", parent=styles["Normal"], fontSize=28, textColor=colors.HexColor("#dc2626"), alignment=TA_CENTER, leading=32))
    story=[Paragraph("SaúdeApp",styles["TituloSaude"]), Paragraph(titulo,styles["Heading2"]), Paragraph(subtitulo,styles["Sub"]), Spacer(1,14), Paragraph(translate("docs.simulated_notice"),styles["Water"]), Spacer(1,12)]
    return doc,buf,story,styles


def _qr(url):
    qr=qrcode.QRCode(version=1,box_size=4,border=2); qr.add_data(url); qr.make(fit=True)
    img=qr.make_image(); b=BytesIO(); img.save(b,format="PNG"); b.seek(0); return Image(b,width=78,height=78)


def _rodape(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica",8); canvas.setFillColor(colors.HexColor("#64748b")); canvas.drawCentredString(A4[0]/2,22,translate("docs.footer")); canvas.restoreState()


def _tabela(data, widths=None):
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#eff6ff")),("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#1d4ed8")),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("GRID",(0,0),(-1,-1),.4,colors.HexColor("#cbd5e1")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t


def _finalizar(doc,buf,story,verification_url=None):
    if verification_url:
        story += [Spacer(1,14), Paragraph(translate("docs.demo_code"), getSampleStyleSheet()["Heading3"]), _qr(verification_url), Paragraph(translate("docs.qr_instruction"), getSampleStyleSheet()["Normal"])]
    doc.build(story,onFirstPage=_rodape,onLaterPages=_rodape); return buf.getvalue()


def _imc(usuario):
    mapa={
        "Abaixo do peso":"dash.underweight", "Peso normal":"dash.normal_weight", "Sobrepeso":"dash.overweight",
        "Obesidade grau I":"dash.obesity_1", "Obesidade grau II":"dash.obesity_2", "Obesidade grau III":"dash.obesity_3",
    }
    return translate(mapa.get(usuario.classificar_imc(), "dash.no_records"))


def gerar_resumo(usuario, verification_url=None):
    doc,buf,story,styles=_pdf_base(translate("docs.health_summary"),f"{translate('docs.patient')}: {usuario.nome or usuario.login} • {translate('docs.generated_at')} {datetime.now():%d/%m/%Y %H:%M}")
    dados=[[translate("docs.field"),translate("docs.information")],[translate("docs.patient"),usuario.nome or usuario.login],[translate("docs.age"),f"{usuario.idade} {translate('docs.years')}"],[translate("docs.blood_type"),usuario.tipo_sanguineo or translate("docs.not_informed")],[translate("docs.height"),f"{usuario.altura:.2f} m"],[translate("docs.weight"),f"{usuario.peso:.1f} kg"],["IMC",f"{usuario.calcular_imc():.2f} — {_imc(usuario)}"],[translate("docs.water_goal"),f"{usuario.meta_agua:.1f} L/{translate('docs.day')}"]]
    story += [_tabela(dados,[150,320]),Spacer(1,16),Paragraph(translate("docs.latest_measurements"),styles["Heading3"])]
    p=usuario.ultima_pressao(); g=usuario.ultima_glicemia()
    story += [_tabela([[translate("docs.measurement"),translate("docs.value")],[translate("docs.pressure"),f"{p['sistolica']}/{p['diastolica']} mmHg" if p else translate("docs.not_recorded")],[translate("docs.glucose"),f"{g['valor']} mg/dL" if g else translate("docs.not_recorded")],[translate("docs.water_today"),f"{usuario.agua_consumida:.1f} L"]],[150,320])]
    return _finalizar(doc,buf,story,verification_url)


def gerar_receita(usuario, receita, verification_url=None):
    doc,buf,story,styles=_pdf_base(translate("docs.prescription_demo"),f"{translate('docs.patient')}: {usuario.nome or usuario.login} • {translate('docs.date')}: {receita['data']}")
    story += [Paragraph(f"{translate('docs.professional')}: Dr(a). {receita['medico']} • CRM: {receita.get('crm') or translate('docs.not_informed')}",styles["Normal"]),Spacer(1,12)]
    rows=[[translate("docs.medication"),translate("docs.dosage"),translate("docs.frequency"),translate("docs.duration")]]+[[m["nome"],m.get("dosagem","") ,m.get("frequencia","") ,m.get("duracao","")] for m in receita.get("medicamentos",[])]
    story += [_tabela(rows,[150,100,130,90]),Spacer(1,20),Paragraph(translate("docs.prescription_note"),styles["Normal"])]
    return _finalizar(doc,buf,story,verification_url)


def gerar_agendamento(usuario, agendamento, verification_url=None):
    doc,buf,story,styles=_pdf_base(translate("docs.appointment_demo"),f"{translate('docs.patient')}: {usuario.nome or usuario.login}")
    status=agendamento.get('status','agendado')
    status_map={'agendado':translate('docs.scheduled'),'cancelado':translate('docs.cancelled'),'realizado':translate('docs.completed')}
    rows=[[translate("docs.field"),translate("docs.information")],[translate("docs.professional"),f"Dr(a). {agendamento['medico']}"],[translate("docs.specialty"),agendamento['especialidade']],[translate("docs.date"),agendamento['data_consulta']],[translate("docs.time"),agendamento['hora']],[translate("docs.location"),agendamento.get('local') or translate('docs.not_informed')],[translate("docs.status"),status_map.get(status,status.upper())]]
    story += [_tabela(rows,[150,320]),Spacer(1,20),Paragraph(translate("docs.appointment_note"),styles["Normal"])]
    return _finalizar(doc,buf,story,verification_url)


def gerar_exame(usuario, exame, verification_url=None):
    doc,buf,story,styles=_pdf_base(translate("docs.exam_demo"),f"{translate('docs.patient')}: {usuario.nome or usuario.login} • {translate('docs.date')}: {exame['data']}")
    rows=[[translate("docs.field"),translate("docs.information")],[translate("docs.exam"),exame['tipo']],[translate("docs.result"),exame.get('resultado') or translate('docs.not_informed')],[translate("docs.notes"),exame.get('observacoes') or translate('docs.not_informed')],[translate("docs.file"),exame.get('arquivo') or translate('docs.no_file')]]
    story += [_tabela(rows,[150,320]),Spacer(1,18),Paragraph(translate("docs.exam_note"),styles["Normal"])]
    return _finalizar(doc,buf,story,verification_url)


def gerar_carteirinha(usuario, verification_url=None):
    doc,buf,story,styles=_pdf_base(translate("docs.patient_card"),f"{translate('docs.internal_registration')} • {datetime.now():%d/%m/%Y}")
    dados=[[translate("docs.field"),translate("docs.information")],[translate("docs.name"),usuario.nome or usuario.login],[translate("docs.identifier"),usuario.login],[translate("docs.blood_type"),usuario.tipo_sanguineo or translate("docs.not_informed")],[translate("docs.age"),f"{usuario.idade} {translate('docs.years')}"]]
    story += [_tabela(dados,[150,320]),Spacer(1,18),Paragraph(translate("docs.card_note"),styles["Normal"])]
    return _finalizar(doc,buf,story,verification_url)


def criar_token(login,tipo,referencia_id=None):
    token=secrets.token_urlsafe(12)
    banco.registrar_documento(token,login,tipo,referencia_id)
    return token
