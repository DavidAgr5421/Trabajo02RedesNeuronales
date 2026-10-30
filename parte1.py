# -*- coding: utf-8 -*-
"""
Punto de entrada principal para la Parte 1: Probabilidad de Incumplimiento (PD).
Redirige la ejecución a 'parte_1/parte1.py'.

Uso:
    python parte1.py
    o
    python parte_1/parte1.py
"""
from pathlib import Path
import runpy

script_target = Path(__file__).resolve().parent / "parte_1" / "parte1.py"

if not script_target.exists():
    raise FileNotFoundError(f"No se encontró el script en {script_target}")

runpy.run_path(str(script_target), run_name="__main__")
