
import datetime
import uuid

def gerar_numero_processo():
    ano = datetime.datetime.now().year
    uid = str(uuid.uuid4())[:8]
    return f"PROC-AMB-{ano}-{uid}"
