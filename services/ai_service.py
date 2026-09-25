"""Integração opcional com IA.

A aplicação continua funcionando sem uma chave de API. Quando OPENAI_API_KEY
estiver configurada, o Assistente usa a Responses API da OpenAI.
"""
import os
from datetime import date, datetime
from services.i18n import translate

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def _resumo_usuario(usuario):
    proximas = sorted(
        [a for a in usuario.agendamentos if a.get("status") == "agendado"],
        key=lambda a: (a.get("data_consulta", ""), a.get("hora", ""))
    )[:5]
    return {
        "nome": usuario.nome or usuario.login,
        "idade": usuario.idade,
        "peso": usuario.peso,
        "altura": usuario.altura,
        "tipo_sanguineo": usuario.tipo_sanguineo,
        "meta_agua": usuario.meta_agua,
        "agua_consumida": usuario.agua_consumida,
        "proximos_agendamentos": proximas,
        "ultimas_consultas": usuario.consultas[-5:],
        "ultimos_exames": usuario.exames[:5],
        "ultimas_pressao": usuario.historico_pressao[-5:],
        "ultimas_glicemia": usuario.historico_glicemia[-5:],
        "ultimos_pesos": usuario.historico_peso[-5:],
        "alergias": usuario.alergias,
        "doencas_cronicas": usuario.doencas_cronicas,
        "medicamentos_continuos": usuario.medicamentos_continuos,
    }

def perguntar(usuario, pergunta, idioma="pt-BR"):
    if not pergunta or len(pergunta.strip()) < 2:
        return False, translate("ai.empty_question")

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return False, translate("ai.not_configured")

    if OpenAI is None:
        return False, translate("ai.library_missing")

    modelo = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
    contexto = _resumo_usuario(usuario)

    instrucoes = f"""
Você é o Assistente do SaúdeApp, um sistema acadêmico de organização de informações de saúde.
Data atual: {date.today().isoformat()}.
Idioma da resposta: {idioma}.

Você pode:
- explicar os dados já registrados pelo usuário;
- resumir consultas, exames, receitas e agendamentos;
- ajudar a organizar perguntas para uma consulta;
- explicar conceitos gerais de saúde em linguagem simples;
- apontar quando uma informação parece merecer atenção, sem diagnosticar.

Regras de segurança:
- Não faça diagnóstico.
- Não prescreva, altere ou suspenda medicamentos.
- Não trate seus cálculos como avaliação médica.
- Para sintomas graves ou emergência, oriente procurar atendimento profissional/serviço de emergência.
- Nunca invente dados que não estejam no contexto.
- Diferencie claramente fato registrado de orientação geral.
- Não revele senha, token, credenciais ou segredos internos.
- Responda de forma curta, clara e útil.

Dados disponíveis do usuário:
{contexto}
"""

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=modelo,
            instructions=instrucoes,
            input=pergunta.strip(),
        )
        texto = getattr(response, "output_text", None)
        if not texto:
            return False, translate("ai.no_response")
        return True, texto.strip()
    except Exception as exc:
        # Não expõe detalhes potencialmente sensíveis da exceção ao usuário.
        return False, translate("ai.request_failed")
