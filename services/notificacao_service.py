from __future__ import annotations
from datetime import datetime
from database import banco
from utils.tempo import agora


def sincronizar(usuario):
    # Alertas clínicos calculados pelo próprio sistema.
    for i, alerta in enumerate(usuario.gerar_alertas()):
        banco.criar_notificacao(
            usuario.login,
            f'alerta:{agora().date().isoformat()}:{i}:{alerta["mensagem"]}',
            'Atenção no acompanhamento',
            alerta['mensagem'],
            alerta['tipo'],
        )

    futuros = usuario.agendamentos_futuros()
    for a in futuros:
        try:
            dt = datetime.strptime(f'{a["data_consulta"]} {a["hora"]}', '%Y-%m-%d %H:%M')
        except ValueError:
            continue
        delta = dt - agora().replace(tzinfo=None)
        if 0 <= delta.total_seconds() <= 48 * 3600:
            banco.criar_notificacao(
                usuario.login,
                f'agendamento:{a["id"]}:48h',
                'Consulta próxima',
                f'{a["especialidade"]} com {a["medico"]} em {a["data_consulta"]} às {a["hora"]}.',
                'info',
            )


def listar(login):
    return banco.listar_notificacoes(login)


def nao_lidas(login):
    return banco.contar_nao_lidas(login)
