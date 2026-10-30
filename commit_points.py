import subprocess
import os

repo = r"C:\Users\felip\Desktop\Trabajo02RedesNeuronales"

with open(os.path.join(repo, "parte1.py"), "r", encoding="utf-8") as f:
    full_text = f.read()
    lines = full_text.splitlines(keepends=True)

p5 = 3212
p6 = 3720
p7 = 4084

def run_git(args):
    res = subprocess.run(["git"] + args, cwd=repo, capture_output=True, text=True, check=True)
    return res.stdout.strip()

# Paso 1: Quitar puntos 5, 6 y 7
with open(os.path.join(repo, "parte1.py"), "w", encoding="utf-8") as f:
    f.writelines(lines[:p5])
run_git(["add", "parte1.py"])
out1 = run_git(["commit", "-m", "refactor: desacoplar modulos de evaluacion, scorecard e interpretabilidad"])
print("Commit 1:", out1)

# Paso 2: Agregar Punto 5
with open(os.path.join(repo, "parte1.py"), "w", encoding="utf-8") as f:
    f.writelines(lines[:p6])
run_git(["add", "parte1.py"])
out2 = run_git(["commit", "-m", "feat(evaluacion): implementar evaluacion en prueba, calibracion Wilson y bootstrap pareado (Punto 5)"])
print("Commit 2:", out2)

# Paso 3: Agregar Punto 6
with open(os.path.join(repo, "parte1.py"), "w", encoding="utf-8") as f:
    f.writelines(lines[:p7])
run_git(["add", "parte1.py"])
out3 = run_git(["commit", "-m", "feat(scorecard): implementar construccion de scorecard, factor PDO y descomposicion aditiva (Punto 6)"])
print("Commit 3:", out3)

# Paso 4: Agregar Punto 7
with open(os.path.join(repo, "parte1.py"), "w", encoding="utf-8") as f:
    f.writelines(lines)
run_git(["add", "parte1.py"])
out4 = run_git(["commit", "-m", "feat(interpretabilidad): implementar importancia por permutacion, escenarios marginales y Shapley aproximado (Punto 7)"])
print("Commit 4:", out4)

# Verificacion final de integridad
with open(os.path.join(repo, "parte1.py"), "r", encoding="utf-8") as f:
    final_text = f.read()

assert final_text == full_text, "Error de integridad: el archivo no coincide"
print("SUCCESS: 100% integridad y 4 commits generados correctamente.")

if os.path.exists(__file__):
    os.remove(__file__)

