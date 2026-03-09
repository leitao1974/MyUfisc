import json
from shapely.geometry import shape, Point
from config import Config


def carregar_geojson(path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


ren_layer = carregar_geojson(Config.REN_LAYER)
ran_layer = carregar_geojson(Config.RAN_LAYER)
natura_layer = carregar_geojson(Config.NATURA_LAYER)


def verificar_geojson(layer, ponto):

    if not layer:
        return False

    for feature in layer["features"]:

        geom = shape(feature["geometry"])

        if geom.contains(ponto):
            return True

    return False


def verificar_camadas(lat, lon):

    ponto = Point(lon, lat)

    return {

        "REN": verificar_geojson(ren_layer, ponto),
        "RAN": verificar_geojson(ran_layer, ponto),
        "NATURA2000": verificar_geojson(natura_layer, ponto)

    }
