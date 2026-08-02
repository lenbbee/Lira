# 🌌 LIRA — Exoplanet Radar System

Radar táctico interactivo para visualizar exoplanetas habitables en tiempo real, con datos oficiales del **NASA Exoplanet Archive**.

## 🚀 Características

- 📡 **API de NASA** con caché offline en JSON.
- 🧮 **Conversión polar → cartesiana** en tiempo real con zoom dinámico.
- 📊 **Clustering climático** por temperatura y densidad: 🟢 Oasis Templados · 🔵 Mundos Glaciales · 🟠 Invernaderos Cálidos.
- 🖥️ **Interfaz cyberpunk** en CustomTkinter con selección por clic (distancia euclidiana).

## 🛠️ Tecnologías

Python 3.12 · CustomTkinter · Requests · Pytest

## 📦 Instalación y uso

```bash
git clone https://github.com/tu-usuario/lira.git
cd lira
pip install -r requirements.txt
python main.py
```

La primera ejecución descarga los datos desde la NASA y los guarda en `data/exoplanets_cache.json`; las siguientes ejecuciones funcionan offline.

## 📁 Estructura

```text
lira/
├── data/
│   └── exoplanets_cache.json   # Caché local de datos NASA
├── src/
│   ├── __init__.py
│   ├── data_manager.py         # API y caché NASA
│   ├── radar_math.py           # Conversión polar-cartesiana
│   ├── clustering.py           # Clasificación de mundos
│   └── interface.py            # GUI CustomTkinter
├── tests/
│   ├── test_data.py            # Pruebas de datos y filtros
│   └── test_math.py            # Pruebas de conversión del radar
├── conftest.py                 # Configuración de pytest
├── main.py                     # Punto de entrada
├── requirements.txt
└── .gitignore
```

## 🧪 Tests

```bash
pytest
```

La suite verifica la conexión con los datos de la NASA, el filtrado de exoplanetas habitables y las conversiones matemáticas del radar.

## 📄 Licencia

MIT. Datos por el [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).