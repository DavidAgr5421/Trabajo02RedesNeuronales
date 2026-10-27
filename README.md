# Trabajo 2: Redes Neuronales para Datos Tabulares (¿Me Prestas?)

**Curso:** Redes Neuronales y Algoritmos Bioinspirados  
**Institución:** Universidad Nacional de Colombia — Facultad de Minas  
**Semestre:** 2026-02  
**Dataset original:** [Lending Club - Credit Risk Analysis (Kaggle)](https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset)

---

## 📌 Descripción del Proyecto

Este repositorio contiene la solución técnica y reproducible para la evaluación de riesgo crediticio en créditos de consumo de Lending Club:
1. **Parte 1 (Clasificación binaria):** Estimación de la Probabilidad de Incumplimiento ($PD$) mediante un Perceptrón Multicapa (`MLPClassifier`), calibración probabilística (Brier, Curva de Calibración) y construcción de la Scorecard oficial ($S_0=600$, $Odds_0=20$, $PDO=50$).
2. **Parte 2 (Regresión continua):** Modelado de la Pérdida Dado el Incumplimiento ($LGD$) acotada en $[0, 1]$ mediante `MLPRegressor` sobre créditos castigados y cálculo de la Pérdida Esperada agregada:
   $$\mathbb{E}[L] = PD \times LGD \times EAD$$
3. **Aplicación Web:** Sistema interactivo en Streamlit con diseño dark-tech para inferencia en tiempo real, velocímetro de scoring, comparativa poblacional y simulador de sensibilidad *"What-if"*.

---

## 🚀 Ejecución Rápida en 1 Solo Comando

### 1. Aplicación Web (Sin reentrenar)
La aplicación web utiliza directamente los modelos preentrenados almacenados en la carpeta `modelos/`:
* **En Windows:**
  ```cmd
  run_app.bat
  ```
* **En Linux / Mac / Git Bash:**
  ```bash
  bash run_app.sh
  ```
  *(O directamente: `python -m streamlit run app.py`)*

### 2. Entrenamiento y Regeneración de Modelos Offline (< 15 segundos)
Para regenerar y validar todos los modelos desde los datos procesados sin requerir conexión a internet ni descargar archivos externos:
```cmd
python exportar_artefactos.py
```

---

## ⚙️ Instalación y Entorno Reproducible

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Trabajo02RedesNeuronales
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / Mac:
   source .venv/bin/activate
   ```

3. Instalar las dependencias con versiones fijas:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💾 Datos Procesados y Reproducibilidad Offline

Cumpliendo con la exigencia del entregable de **no depender de APIs externas ni descargas pesadas de internet**:
* Se incluye en el repositorio la base procesada comprimida:
  [`datos/base_procesada_cohorte.csv.gz`](file:///D:/Estudio/NACHO/10mo%20Semestre/Redes/Entrega2/Trabajo02RedesNeuronales/datos/base_procesada_cohorte.csv.gz) (~2.19 MB).
* **Cómo se obtuvo:**
  * Del dataset original `loan.csv` (887,379 registros), se filtró la cohorte principal de créditos a 36 meses originados hasta diciembre de 2012 con etiqueta válida según la regla del enunciado (74,959 créditos).
  * Se asignaron las particiones temporales congeladas:
    * **Entrenamiento (`train`):** Junio 2007 a Diciembre 2011 (31,534 créditos).
    * **Validación (`validation`):** Enero a Junio 2012 (14,967 créditos).
    * **Prueba (`test`):** Julio a Diciembre 2012 (28,458 créditos).
  * Se calcularon los atributos derivados en originación (`credit_history_years`, limpieza de `revol_util`) y se conservaron los campos financieros para $LGD$ y $EAD$.

---

## 🎲 Semillas Aleatorias y Comparación Justa

* **Semilla fija predeterminada:** `42` (utilizada para inferencia individual, preprocesamiento y modelo de referencia).
* **Evaluación de variabilidad:** Entrenamientos independientes evaluados sobre **30 semillas consecutivas (42 a 71)** reportando Media, Desviación Estándar, Mejor y Peor desempeño en validación y prueba.

---

## 📦 Estructura del Repositorio

```text
Trabajo02RedesNeuronales/
├── app.py                      # Aplicación Web en Streamlit (Dark-Tech)
├── exportar_artefactos.py      # Rutina autónoma de entrenamiento y exportación offline
├── parte1.py                   # Script completo de la Parte 1 (PD, Scorecard, Interpretabilidad)
├── Parte_2_Trabajo_2.py        # Script completo de la Parte 2 (LGD y Pérdida Esperada)
├── requirements.txt            # Dependencias fijas reproducibles
├── run_app.bat                 # Script de arranque en Windows (1 comando)
├── run_app.sh                  # Script de arranque en Linux/Mac (1 comando)
├── README.md                   # Documentación y guía de ejecución
├── datos/
│   └── base_procesada_cohorte.csv.gz # Dataset procesado offline (2.19 MB, 74,959 filas)
└── modelos/                    # Artefactos entrenados serializados
    ├── preprocesador.joblib    # ColumnTransformer ajustado en train
    ├── mlp_pd.joblib           # MLPClassifier (Probabilidad de Incumplimiento)
    ├── mlp_lgd.joblib          # MLPRegressor (LGD en [0, 1])
    ├── referencia_percentil_train.npz # Puntajes históricos para percentiles
    └── config_scorecard.json   # Parámetros oficiales S0=600, Odds0=20, PDO=50
```

---

## 🌐 Despliegue en Streamlit Community Cloud

1. Sube este repositorio a **GitHub**.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con GitHub.
3. Haz clic en **"New app"**, selecciona este repositorio, la rama `main` y define el archivo principal como `app.py`.
4. Haz clic en **Deploy**. La aplicación estará disponible en línea con URL pública.
