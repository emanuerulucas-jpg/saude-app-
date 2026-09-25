from datetime import datetime
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("America/Sao_Paulo")

def agora():
    return datetime.now(FUSO)

def hoje():
    return agora().date().isoformat()
