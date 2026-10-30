# Parte 2: Pérdida Dado el Incumplimiento (LGD - Regresión) y Pérdida Esperada

En este módulo se desarrolla el modelado continuo de la **Pérdida Dado el Incumplimiento (LGD)** sobre los créditos que efectivamente cayeron en mora, y el cálculo de la **Pérdida Esperada agregada ($E[L]$)** sobre la cartera de prueba.

---

## 📂 Contenido del Módulo

* **`Parte_2_Trabajo_2.py`**: Script completo y autónomo que cubre los puntos requeridos:
  1. **Variable objetivo LGD**: 
     $$\text{LGD} = 1 - \frac{\text{total\_rec\_prncp} + \text{recoveries} - \text{collection\_recovery\_fee}}{\text{funded\_amnt}}$$
     Acotada estrictamente a $[0, 1]$. Justificación de denominadores y discusión de limitaciones (`out_prncp = 0` en créditos castigados).
  2. **Modelo de referencia**: Regresión lineal continua sobre los créditos incumplidos.
  3. **Red neuronal (MLP LGD)**: Optimización de hiperparámetros (arquitectura, activación, alpha, tasa de aprendizaje) con función de pérdida MSE y salida acotada en $[0, 1]$.
  4. **Regla de comparación justa**: Presupuesto de búsqueda explícito y evaluación de variabilidad sobre **30 semillas independientes** (reportando media, desviación estándar, mejor y peor desempeño).
  5. **Evaluación**: Comparación de MAE y RMSE frente a la referencia, y análisis de distribuciones (predicha vs observada).
  6. **Pérdida Esperada ($E[L]$)**: 
     $$\mathbb{E}[L] = \text{PD} \times \text{LGD} \times \text{EAD}$$
     con $\text{EAD} = \text{funded\_amnt}$ sobre los 28.458 créditos del conjunto de prueba.
* **`salida_figura_8_distribucion_lgd.png`**: Gráfica generada comparando la densidad observada de LGD frente a las predicciones de la Regresión Lineal y el MLP LGD.

---

## 🚀 Ejecución

```bash
# Ejecutar desde la raíz:
python Parte_2_Trabajo_2.py

# O ejecutar directamente desde esta carpeta:
python parte_2/Parte_2_Trabajo_2.py
```
