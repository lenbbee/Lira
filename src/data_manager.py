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
        
        # Printeamos los primeros 300 caracteres de lo que sea que mandó la NASA
        print(f"📄 Primeros caracteres recibidos:\n{respuesta.text[:300]}")
        
        if respuesta.status_code == 200:
            return respuesta.json()
            
    except Exception as e:
        print(f"⚠️ Falló la ejecución dentro de descargar_datos_nasa: {e}")
    return []

def obtener_exoplanetas() -> list:
    try: 
        if os.path.exists(CACHE_FILE): #abres el archivo para ver si esta guardado
            with open(CACHE_FILE, "r") as f: #explicame esta linea
                datos = json.load(f) #se escribe en formato json
                return datos # se retorna los datos
        else:
            datos = descargar_datos_nasa() #se desdcargan los datos
            with open (CACHE_FILE, "w") as f: #explicmame esta linea que es w y f
                json.dump(datos, f, indent=4) #se empujan a los datos, aunq explicame esta linea
            return datos
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

# 2. Control de calidad para los datos que a veces vienen vacíos (None)
        # Si la temperatura o la densidad son None, les asignamos un valor por defecto
        # o una estimación teórica para que tu lógica de filtros no colapse.
        if temperatura is None:
            temperatura = 250.0  # Estimación teórica templada por defecto
            
        if densidad is None:
            densidad = 4.0  # Estimación de densidad rocosa por defecto
            
        # 3. Aplicamos tus filtros científicos de la Fase 1
        # Distancia <= 200, Temperatura entre 200 y 300, Densidad entre 3.5 y 5.5
        if (distancia <= 200.0) and (200.0 <= temperatura <= 300.0) and (3.5 <= densidad <= 5.5):
            
            # Si pasa todas las pruebas, lo guardamos en un nuevo diccionario limpio
            # Al que además le agregamos una etiqueta para que tu interfaz sepa qué tipo de planeta es
            planeta_filtrado = {
                "name": nombre,
                "dist": distancia,
                "temp": temperatura,
                "dens": densidad,
                "tipo": "Rocoso Habitable"  # Esta etiqueta servirá para el Pixel Art después
            }
            planetas_habitables.append(planeta_filtrado)
            
    return planetas_habitables