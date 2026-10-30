# Módulo de Sustentación Oral: Demostración y Modificación en Vivo

Este módulo está especialmente diseñado para cumplir con los requerimientos estrictos de la **Sustentación Oral** del Trabajo 2:
1. **Demostración en vivo (< 2 minutos)**: Un solo comando para reentrenar y evaluar el modelo en segundos sobre datos offline.
2. **Modificación en vivo (3 minutos)**: Capacidad de cambiar cualquier parámetro (arquitectura, tasa de aprendizaje, activación, regularización, escala scorecard) desde CLI o archivo de configuración sin tocar el código fuente.

---

## 📂 Contenido del Módulo

* **`ejecutar_experimento.py`**: Motor parametrizado con `argparse` y cálculo instantáneo de métricas (AUC, Gini, KS, Brier, BCE, Scorecard).
* **`config_demo.json`**: Archivo de configuración rápida en JSON.
* **`salida_experimento.json`**: Registro estructurado de la última corrida experimental.

---

## 🚀 Comandos para la Sustentación

### 1. Demostración en 1 solo comando (< 2 segundos de ejecución)
```cmd
# Windows:
run_experimento.bat

# Linux / Mac:
bash run_experimento.sh
```

### 2. Modificación de parámetros solicitada por el profesor
Ejemplo: Cambiar arquitectura a 64-32 neuronas, activación tangente hiperbólica y tasa de aprendizaje a 0.001:
```cmd
run_experimento.bat --capas 64 32 --activacion tanh --lr 0.001
```

Ejemplo: Cambiar parámetros de la Scorecard ($S_0 = 650$, $\text{PDO} = 40$):
```cmd
run_experimento.bat --s0 650 --pdo 40
```

Ejemplo: Cargar configuración desde un archivo JSON:
```cmd
run_experimento.bat --config sustentacion/config_demo.json
```
