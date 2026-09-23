import json
import os
import requests

CACHE_FILE = "data/exoplanets_cache.json"



NASA_API_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
)

PARAMS = {
    "query": "select pl_name,sy_dist,pl_eqt,pl_dens from pscomppars where sy_dist is not null",
    "format": "json",
}


def descargar_datos_nasa() -> list:
    try:
        respuesta = requests.get(NASA_API_URL, params=PARAMS, timeout=60)
        
        print(f"📡 Código de respuesta del servidor: {respuesta.status_code}")
        
        print(f"📄 Primeros caracteres recibidos:\n{respuesta.text[:300]}")
        
        if respuesta.status_code == 200:
            return respuesta.json()
            
    except Exception as e:
        print(f"⚠️ Falló la ejecución dentro de descargar_datos_nasa: {e}")
    return []

def obtener_exoplanetas() -> list:
    try: 
        if os.path.exists(CACHE_FILE): 
            with open(CACHE_FILE, "r") as f:
                datos = json.load(f) 
                return datos 
        else:
            datos = descargar_datos_nasa() 
            os.makedirs("data", exist_ok=True)
            with open (CACHE_FILE, "w") as f: 
                json.dump(datos, f, indent=4) 
    except Exception as e: #para cerrar el try
        print(f"Error al obtener los datos: {e}")
        return []

def filtrar_habitables(exoplanetas: list) -> list:

    planetas_habitables = []

    for planeta in exoplanetas:
        nombre = planeta.get("pl_name")
        distancia = planeta.get("sy_dist")
        temperatura = planeta.get("pl_eqt")
        densidad = planeta.get("pl_dens")

        if temperatura is None:
            temperatura = 250.0 
        if densidad is None:
            densidad = 4.0 
        
        if (distancia <= 200.0) and (200.0 <= temperatura <= 300.0) and (3.5 <= densidad <= 5.5):
            
            planeta_filtrado = {
                "name": nombre,
                "dist": distancia,
                "temp": temperatura,
                "dens": densidad,
                "tipo": "Rocoso Habitable"  
            }
            planetas_habitables.append(planeta_filtrado)
            
    return planetas_habitables