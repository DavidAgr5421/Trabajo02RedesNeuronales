# -*- coding: utf-8 -*-
"""
Punto de entrada principal para la Parte 2: LGD y Pérdida Esperada.
Redirige la ejecución a 'parte_2/Parte_2_Trabajo_2.py'.

Uso:
    python Parte_2_Trabajo_2.py
    o
    python parte_2/Parte_2_Trabajo_2.py
"""
from pathlib import Path
import runpy

script_target = Path(__file__).resolve().parent / "parte_2" / "Parte_2_Trabajo_2.py"

if not script_target.exists():
    raise FileNotFoundError(f"No se encontró el script en {script_target}")

runpy.run_path(str(script_target), run_name="__main__")
