
def avaliar_infracao(camadas):

    regimes = []

    if camadas.get("REN"):
        regimes.append({
            "regime": "Reserva Ecológica Nacional",
            "diploma": "DL 166/2008",
            "artigo": "Art. 20.º"
        })

    if camadas.get("RAN"):
        regimes.append({
            "regime": "Reserva Agrícola Nacional",
            "diploma": "DL 73/2009",
            "artigo": "Art. 22.º"
        })

    if camadas.get("NATURA2000"):
        regimes.append({
            "regime": "Rede Natura 2000",
            "diploma": "DL 140/99",
            "artigo": "Art. 9.º"
        })

    return regimes
