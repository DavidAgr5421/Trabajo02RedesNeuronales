# -*- coding: utf-8 -*-
"""
Punto de entrada principal para la Aplicación Web en Streamlit.
Ejecuta la aplicación ubicada en la carpeta 'app_streamlit/app.py'.

Uso:
    streamlit run app.py
    o
    streamlit run app_streamlit/app.py
"""
import sys
from pathlib import Path
import runpy

app_target = Path(__file__).resolve().parent / "app_streamlit" / "app.py"

if not app_target.exists():
    raise FileNotFoundError(f"No se encontró el script de la app en {app_target}")

runpy.run_path(str(app_target), run_name="__main__")
