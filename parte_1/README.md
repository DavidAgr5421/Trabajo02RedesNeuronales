# Parte 1: Probabilidad de Incumplimiento (Clasificación Binaria)

En este módulo se desarrolla el modelado de la **Probabilidad de Incumplimiento (PD)** para solicitantes de crédito de consumo en Lending Club.

---

## 📂 Contenido del Módulo

* **`parte1.py`**: Script completo y autónomo con la implementación de las Tareas 1 a 7:
  1. **Caso de uso**: Analista de riesgo evaluando solicitudes en originación sin fuga de información (*data leakage*).
  2. **Análisis descriptivo e hipótesis**: Formulación y contrastación de hipótesis sobre DTI, utilización rotativa, moras anteriores e historial crediticio.
  3. **Modelo de referencia**: Regresión logística de baja complejidad.
  4. **Red neuronal (MLP)**: Perceptrón multicapa optimizado con búsqueda de hiperparámetros (capas, activación, optimizador Adam, regularización $L_2$ y early stopping).
  5. **Evaluación temporal**: Partición estricta según fecha de originación (Train: 2007–2011, Validation: 2012-1, Test: 2012-2), evaluando discriminación (AUC, Gini, KS) y calibración (Brier Score, curva de calibración).
  6. **Scorecard**: Derivación matemática formal con escala $S_0 = 600$, $\text{Odds}_0 = 20:1$, $\text{PDO} = 50$, descomposición aditiva para el modelo lineal y percentiles poblacionales.
  7. **Interpretabilidad**: Permutation Feature Importance (Fisher et al., 2019), escenarios marginales y aproximación de valores Shapley (Lundberg & Lee, 2017).

---

## 🚀 Ejecución

```bash
# Ejecutar desde la raíz:
python parte1.py

# O ejecutar directamente desde esta carpeta:
python parte_1/parte1.py
```
