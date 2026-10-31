# Trabajo 2: Redes Neuronales para Datos Tabulares (¿Me Prestas?)

**Curso:** Redes Neuronales y Algoritmos Bioinspirados  
**Institución:** Universidad Nacional de Colombia — Facultad de Minas  
**Semestre:** 2026-02  
**Dataset original:** [Lending Club - Credit Risk Analysis (Kaggle)](https://www.kaggle.com/datasets/ranadeep/credit-risk-dataset)  
**Reporte Técnico (GitHub Pages):** [https://davidagr5421.github.io/Trabajo02RedesNeuronales/](https://davidagr5421.github.io/Trabajo02RedesNeuronales/)

---

## 📌 Organización Modular del Repositorio

El proyecto ha sido estructurado en módulos y carpetas independientes para cada componente del trabajo:

```text
Trabajo02RedesNeuronales/
├── parte_1/                  # PARTE 1: Probabilidad de Incumplimiento (PD)
│   ├── parte1.py             # Script completo (Tareas 1 a 7)
│   └── README.md             # Guía metodológica, scorecard e interpretabilidad
│
├── parte_2/                  # PARTE 2: Pérdida Dado el Incumplimiento (LGD)
│   ├── Parte_2_Trabajo_2.py  # Script completo (LGD, 30 semillas, E[L])
│   ├── salida_figura_8...png # Gráfica de distribución de LGD
│   └── README.md             # Justificación matemática y evaluación
│
├── app_streamlit/            # APLICACIÓN WEB INTERACTIVA (STREAMLIT)
│   ├── app.py                # Interfaz UI/UX Dark-Tech ¿Me prestas? (Paleta Verde Esmeralda)
│   └── README.md             # Documentación de inferencia y simulación
│
├── sustentacion/             # MÓDULO DE SUSTENTACIÓN ORAL
│   ├── ejecutar_experimento.py # Script de reentrenamiento CLI en caliente
│   ├── config_demo.json      # Configuración de hiperparámetros
│   ├── salida_experimento.json # Métricas de la última corrida
│   └── README.md             # Instrucciones para la defensa en vivo
│
├── docs/                     # GITHUB PAGES (PUBLICACIÓN WEB)
│   ├── index.html            # Informe técnico interactivo
│   ├── assets/               # CSS técnico y figuras metodológicas
│   ├── blog/                 # Publicaciones y blog complementario
│   ├── Trabajo 2 (1).pdf     # Documento formal descargable
│   └── .nojekyll             # Servido directo sin motor Jekyll
│
├── datos/                    # DATOS PROCESADOS OFFLINE
│   └── base_procesada_cohorte.csv.gz # Cohorte filtrada y particionada (74.959 filas)
│
├── modelos/                  # ARTEFACTOS SERIALIZADOS DE REDES NEURONALES
│   ├── preprocesador.joblib  # ColumnTransformer ajustado en train
│   ├── mlp_pd.joblib         # MLPClassifier (Probabilidad de Incumplimiento)
│   ├── mlp_lgd.joblib        # MLPRegressor (LGD en [0, 1])
│   ├── referencia_percentil_train.npz # Puntajes históricos para percentiles
│   └── config_scorecard.json # Parámetros oficiales S0=600, Odds0=20, PDO=50
│
├── salidas_evaluacion/       # RESULTADOS EXPORTADOS
│   └── perdida_esperada_test.csv.gz # Pérdida esperada crédito a crédito en prueba
│
├── run_app.bat / .sh         # Lanzador de la app web (1 solo comando)
├── run_experimento.bat / .sh # Lanzador de sustentación oral (1 solo comando)
├── exportar_artefactos.py    # Pipeline de reentrenamiento y serialización offline
├── requirements.txt          # Dependencias exactas reproducibles
├── index.html                # Redirección raíz hacia docs/ para GitHub Pages
└── .nojekyll                 # Configuración raíz de GitHub Pages
```

---

## ⚡ Ejecución Rápida en 1 Solo Comando

### 1. Aplicación Web Streamlit
La aplicación interactiva utiliza directamente los modelos preentrenados de la carpeta `modelos/`:
* **Windows:**
  ```cmd
  run_app.bat
  ```
* **Linux / Mac:**
  ```bash
  bash run_app.sh
  ```
*(O directamente: `streamlit run app_streamlit/app.py`)*

### 2. Demostración para la Sustentación Oral (< 2 segundos)
Cumpliendo con la exigencia de una corrida de demostración en menos de 2 minutos:
* **Windows:**
  ```cmd
  run_experimento.bat
  ```
* **Linux / Mac:**
  ```bash
  bash run_experimento.sh
  ```

### 3. Modificación de Parámetros en Vivo (3 minutos)
Para responder a peticiones del profesor durante la sustentación sin editar código fuente:
```cmd
run_experimento.bat --capas 64 32 --activacion tanh --lr 0.001 --s0 650 --pdo 40
```

### 4. Reentrenar y Serializar Artefactos Offline (< 10 segundos)
```bash
python exportar_artefactos.py
```

---

## 🔬 Ejecución Individual de Módulos

* **Parte 1 (Clasificación PD, Scorecard, Interpretabilidad):**
  ```bash
  python parte_1/parte1.py
  # O desde la raíz:
  python parte1.py
  ```

* **Parte 2 (Regresión LGD, 30 Semillas, Pérdida Esperada):**
  ```bash
  python parte_2/Parte_2_Trabajo_2.py
  # O desde la raíz:
  python Parte_2_Trabajo_2.py
  ```

---

## 🛠️ Instalación y Entorno

1. Crear y activar entorno virtual:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / Mac:
   source .venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🌐 Publicación en GitHub Pages y Streamlit Community Cloud

* **GitHub Pages:** Publicado en `https://davidagr5421.github.io/Trabajo02RedesNeuronales/` (apuntando a la carpeta `docs/` o a la raíz con `.nojekyll`).
* **Streamlit Cloud:** Compatible seleccionando `app.py` o `app_streamlit/app.py` como archivo principal.
