# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Ejecutor de Experimentos en Vivo (Sustentación).
Redirige la ejecución a 'sustentacion/ejecutar_experimento.py'.

Uso:
    python ejecutar_experimento.py
    o
    python sustentacion/ejecutar_experimento.py
"""
from pathlib import Path
import runpy

script_target = Path(__file__).resolve().parent / "sustentacion" / "ejecutar_experimento.py"

if not script_target.exists():
    raise FileNotFoundError(f"No se encontró el script en {script_target}")

runpy.run_path(str(script_target), run_name="__main__")
