# Aplicación Web: Motor de Scoring Crediticio (Streamlit)

Aplicación web interactiva desarrollada en **Streamlit** con diseño *Dark-Tech* (atmósfera vino tinto/crimson profundo) para la evaluación de riesgo en tiempo real.

---

## 🎯 Capacidades de la Aplicación

1. **Inferencia en Tiempo Real**:
   * Cálculo de la **Probabilidad de Incumplimiento (PD)** mediante el modelo MLP entrenado.
   * Asignación del **Puntaje en la Scorecard** ($S_0 = 600$, $\text{Odds}_0 = 20:1$, $\text{PDO} = 50$).
   * Estimación de la **Pérdida Dado el Incumplimiento (LGD)** y la **Pérdida Esperada ($E[L]$)** para el monto solicitado.
2. **Posicionamiento Poblacional**:
   * Ubicación percentil sobre la cohorte histórica de entrenamiento (31.534 créditos).
3. **Simulador de Sensibilidad ("What-If")**:
   * Visualización interactiva de cómo varía el puntaje crediticio al modificar atributos clave (DTI, uso rotativo, moras previas, antigüedad laboral).
4. **Perfiles de Demostración**:
   * Carga instantánea de perfiles preconfigurados:
     * *Perfil A*: Riesgo Bajo (Excelente).
     * *Perfil B*: Riesgo Moderado (Promedio).
     * *Perfil C*: Riesgo Alto (Crítico).
5. **Enlaces Integrados**:
   * Acceso directo al **Informe Técnico en GitHub Pages** (`https://davidagr5421.github.io/Trabajo02RedesNeuronales/`), repositorio GitHub y video demo.

---

## 🚀 Despliegue y Ejecución

* **En Windows (desde la raíz):**
  ```cmd
  run_app.bat
  ```
* **En Linux / Mac:**
  ```bash
  bash run_app.sh
  ```
* **Directamente con Streamlit:**
  ```bash
  streamlit run app_streamlit/app.py
  # O mediante el punto de entrada raíz:
  streamlit run app.py
  ```
