
import geopandas as gpd
from shapely.geometry import Point
from config import Config

try:
    ren_layer = gpd.read_file(Config.REN_LAYER)
except:
    ren_layer = None

try:
    ran_layer = gpd.read_file(Config.RAN_LAYER)
except:
    ran_layer = None

try:
    natura_layer = gpd.read_file(Config.NATURA_LAYER)
except:
    natura_layer = None

def verificar_camadas(lat, lon):

    ponto = Point(lon, lat)

    resultado = {
        "REN": False,
        "RAN": False,
        "NATURA2000": False
    }

    if ren_layer is not None and not ren_layer[ren_layer.contains(ponto)].empty:
        resultado["REN"] = True

    if ran_layer is not None and not ran_layer[ran_layer.contains(ponto)].empty:
        resultado["RAN"] = True

    if natura_layer is not None and not natura_layer[natura_layer.contains(ponto)].empty:
        resultado["NATURA2000"] = True

    return resultado
