# -*- coding: utf-8 -*-
"""
================================================================================
EJECUTOR DE EXPERIMENTOS EN VIVO — SUSTENTACIÓN ORAL
================================================================================
Permite modificar parámetros de arquitectura, optimizador, regularización
y scorecard desde la línea de comandos (CLI) o archivo JSON sin editar código.
Ejecución completa en menos de 15 segundos sobre la base procesada offline.
================================================================================
"""

import sys
import time
import json
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
from sklearn.neural_network import MLPClassifier
from scipy.stats import ks_2samp

# 1. Configuración de rutas y columnas
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR if (BASE_DIR / "datos").exists() else BASE_DIR.parent
DATOS_PATH = ROOT_DIR / "datos" / "base_procesada_cohorte.csv.gz"
CONFIG_DEFAULT_PATH = BASE_DIR / "config_demo.json" if (BASE_DIR / "config_demo.json").exists() else ROOT_DIR / "config_demo.json"

NUMERICAS = [
    "loan_amnt", "annual_inc", "dti",
    "delinq_2yrs", "inq_last_6mths",
    "open_acc", "pub_rec", "revol_bal",
    "revol_util", "total_acc",
    "credit_history_years"
]

CATEGORICAS = [
    "emp_length",
    "home_ownership",
    "purpose"
]

FEATURES = NUMERICAS + CATEGORICAS

# 2. Argument Parser para la Sustentación
def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Ejecución y modificación de experimentos en vivo (Sustentación Trabajo 2)"
    )
    parser.add_argument("--config", type=str, default=None, help="Ruta a un archivo JSON de configuración")
    parser.add_argument("--capas", type=int, nargs="+", default=None, help="Neuronas por capa oculta, ej: --capas 64 32 16")
    parser.add_argument("--lr", type=float, default=None, help="Tasa de aprendizaje inicial, ej: --lr 0.005")
    parser.add_argument("--activacion", type=str, choices=["relu", "tanh", "logistic"], default=None, help="Función de activación oculta")
    parser.add_argument("--alpha", type=float, default=None, help="Penalización de regularización L2, ej: --alpha 0.01")
    parser.add_argument("--optimizador", type=str, choices=["adam", "sgd"], default=None, help="Optimizador (adam o sgd)")
    parser.add_argument("--epocas", type=int, default=None, help="Número máximo de épocas, ej: --epocas 50")
    parser.add_argument("--paciencia", type=int, default=None, help="Paciencia para parada temprana, ej: --paciencia 8")
    parser.add_argument("--s0", type=float, default=None, help="Puntaje base de la scorecard, ej: --s0 650.0")
    parser.add_argument("--pdo", type=float, default=None, help="Puntos para duplicar las odds (PDO), ej: --pdo 40.0")
    parser.add_argument("--odds0", type=float, default=None, help="Odds de referencia, ej: --odds0 20.0")
    parser.add_argument("--semilla", type=int, default=None, help="Semilla aleatoria del experimento")

    return parser.parse_args()

def cargar_configuracion(args):
    # Cargar valores base desde JSON
    config_file = Path(args.config) if args.config else CONFIG_DEFAULT_PATH
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {
            "arquitectura": [32, 16],
            "activacion": "relu",
            "optimizador": "adam",
            "tasa_aprendizaje": 0.003,
            "regularizacion_alpha": 0.0001,
            "max_epocas": 40,
            "paciencia": 6,
            "batch_size": 256,
            "semilla": 42,
            "scorecard": {"puntaje_base_S0": 600.0, "odds_referencia_Odds0": 20.0, "puntos_duplicar_odds_PDO": 50.0}
        }

    # Sobrescribir con banderas CLI si fueron provistas
    if args.capas is not None:
        cfg["arquitectura"] = list(args.capas)
    if args.lr is not None:
        cfg["tasa_aprendizaje"] = args.lr
    if args.activacion is not None:
        cfg["activacion"] = args.activacion
    if args.alpha is not None:
        cfg["regularizacion_alpha"] = args.alpha
    if args.optimizador is not None:
        cfg["optimizador"] = args.optimizador
    if args.epocas is not None:
        cfg["max_epocas"] = args.epocas
    if args.paciencia is not None:
        cfg["paciencia"] = args.paciencia
    if args.semilla is not None:
        cfg["semilla"] = args.semilla
    if args.s0 is not None:
        cfg["scorecard"]["puntaje_base_S0"] = args.s0
    if args.pdo is not None:
        cfg["scorecard"]["puntos_duplicar_odds_PDO"] = args.pdo
    if args.odds0 is not None:
        cfg["scorecard"]["odds_referencia_Odds0"] = args.odds0

    return cfg

def calcular_estadistico_ks(y_true, y_prob):
    prob_buenos = y_prob[y_true == 0]
    prob_malos = y_prob[y_true == 1]
    res = ks_2samp(prob_malos, prob_buenos)
    return float(res.statistic)

# 3. Función principal de ejecución
def main():
    t_inicio = time.time()
    args = parsear_argumentos()
    cfg = cargar_configuracion(args)

    print("=" * 76)
    print(" EJECUCIÓN DE EXPERIMENTO EN VIVO — SISTEMA DE EVALUACIÓN DE RIESGO")
    print("=" * 76)
    print(f" Arquitectura MLP:        {cfg['arquitectura']}")
    print(f" Función de Activación:   {cfg['activacion']}")
    print(f" Optimizador / Tasa LR:   {cfg['optimizador']} (lr={cfg['tasa_aprendizaje']})")
    print(f" Regularización L2:       alpha={cfg['regularizacion_alpha']}")
    print(f" Parada Temprana:         Paciencia={cfg['paciencia']} épocas (Max {cfg['max_epocas']} épocas)")
    print(f" Semilla aleatoria:       {cfg['semilla']}")
    print(f" Scorecard Parámetros:    S0={cfg['scorecard']['puntaje_base_S0']} pts | Odds0={cfg['scorecard']['odds_referencia_Odds0']}:1 | PDO={cfg['scorecard']['puntos_duplicar_odds_PDO']} pts")
    print("-" * 76)

    # 1. Cargar datos procesados offline
    if not DATOS_PATH.exists():
        print(f"Error: No se encontró el dataset en '{DATOS_PATH}'.")
        print("Ejecuta 'python exportar_artefactos.py' para generarlo.")
        sys.exit(1)

    t_data = time.time()
    cohorte = pd.read_csv(DATOS_PATH, low_memory=False)
    cohorte["target_pd"] = cohorte["target_pd"].astype(int)
    print(f" Dataset offline cargado: {len(cohorte):,} filas en {time.time() - t_data:.2f} s")

    # Separar particiones temporales congeladas
    train = cohorte.loc[cohorte["split"].eq("train")].copy()
    val = cohorte.loc[cohorte["split"].eq("validation")].copy()
    test = cohorte.loc[cohorte["split"].eq("test")].copy()

    # 2. Cargar preprocesador serializado
    preproc_path = BASE_DIR / "modelos" / "preprocesador.joblib"
    if preproc_path.exists():
        import joblib
        preprocesador = joblib.load(preproc_path)
    else:
        from sklearn.compose import ColumnTransformer
        from sklearn.pipeline import Pipeline
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder

        preprocesador = ColumnTransformer(
            transformers=[
                ("num", Pipeline([("imp", SimpleImputer(strategy="median", add_indicator=True)), ("std", StandardScaler())]), NUMERICAS),
                ("cat", Pipeline([("imp", SimpleImputer(strategy="constant", fill_value="Sin dato")), ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), CATEGORICAS)
            ]
        )
        preprocesador.fit(train[FEATURES])

    X_train = np.asarray(preprocesador.transform(train[FEATURES]), dtype=np.float64)
    y_train = train["target_pd"].to_numpy(dtype=np.int64)

    X_val = np.asarray(preprocesador.transform(val[FEATURES]), dtype=np.float64)
    y_val = val["target_pd"].to_numpy(dtype=np.int64)

    X_test = np.asarray(preprocesador.transform(test[FEATURES]), dtype=np.float64)
    y_test = test["target_pd"].to_numpy(dtype=np.int64)

    # 3. Entrenar Perceptrón Multicapa (MLP)
    print(" Entrenando Red Neuronal MLP...")
    t_train = time.time()
    mlp = MLPClassifier(
        hidden_layer_sizes=tuple(cfg["arquitectura"]),
        activation=cfg["activacion"],
        solver=cfg["optimizador"],
        alpha=cfg["regularizacion_alpha"],
        learning_rate_init=cfg["tasa_aprendizaje"],
        max_iter=cfg["max_epocas"],
        batch_size=cfg["batch_size"],
        early_stopping=True,
        n_iter_no_change=cfg["paciencia"],
        random_state=cfg["semilla"]
    )
    mlp.fit(X_train, y_train)
    t_entrenamiento = time.time() - t_train

    # Contar parámetros entrenables
    num_params = sum(w.size for w in mlp.coefs_) + sum(b.size for b in mlp.intercepts_)
    print(f" Entrenamiento finalizado en {t_entrenamiento:.2f} s ({mlp.n_iter_} épocas convergidas, {num_params:,} parámetros).")

    # 4. Inferencia y Evaluación en Validación y Prueba
    prob_val = mlp.predict_proba(X_val)[:, 1]
    prob_test = mlp.predict_proba(X_test)[:, 1]

    # Métricas de Discriminación
    auc_val = float(roc_auc_score(y_val, prob_val))
    gini_val = 2.0 * auc_val - 1.0
    ks_val = calcular_estadistico_ks(y_val, prob_val)

    auc_test = float(roc_auc_score(y_test, prob_test))
    gini_test = 2.0 * auc_test - 1.0
    ks_test = calcular_estadistico_ks(y_test, prob_test)

    # Métricas de Calibración
    brier_val = float(brier_score_loss(y_val, prob_val))
    bce_val = float(log_loss(y_val, prob_val))

    brier_test = float(brier_score_loss(y_test, prob_test))
    bce_test = float(log_loss(y_test, prob_test))

    # 5. Cálculo de Scorecard con Parámetros Configurables
    s0 = cfg["scorecard"]["puntaje_base_S0"]
    odds0 = cfg["scorecard"]["odds_referencia_Odds0"]
    pdo = cfg["scorecard"]["puntos_duplicar_odds_PDO"]

    factor = pdo / np.log(2)
    offset = s0 - factor * np.log(odds0)

    q_test = np.clip(prob_test, 1e-12, 1.0 - 1e-12)
    scores_test = offset + factor * (np.log1p(-q_test) - np.log(q_test))

    # 6. Tabla de Resultados Formateada
    print("\n" + "=" * 76)
    print(" RESUMEN DE RESULTADOS DE EVALUACIÓN")
    print("=" * 76)
    print(f"{'Métrica Evaluada':<32} | {'Validación (14,967)':<18} | {'Prueba (28,458)':<18}")
    print("-" * 76)
    print(f"{'AUC (Área bajo la curva ROC)':<32} | {auc_val:<18.4f} | {auc_test:<18.4f}")
    print(f"{'Coeficiente de Gini':<32} | {gini_val:<18.4f} | {gini_test:<18.4f}")
    print(f"{'Estadístico KS (Separación Max)':<32} | {ks_val:<18.4f} | {ks_test:<18.4f}")
    print(f"{'Brier Score (Calibración MSE)':<32} | {brier_val:<18.5f} | {brier_test:<18.5f}")
    print(f"{'BCE Loss (Entropía Cruzada)':<32} | {bce_val:<18.5f} | {bce_test:<18.5f}")
    print("-" * 76)
    print(f"{'Distribución Scorecard en Prueba':<32} | Min: {scores_test.min():.1f} | Mediana: {np.median(scores_test):.1f} | Max: {scores_test.max():.1f} pts")
    print(f"{'Parámetros Derivados Scorecard':<32} | Factor: {factor:.4f} | Offset: {offset:.4f}")
    print("=" * 76)
    t_total = time.time() - t_inicio
    print(f" Tiempo total de ejecución del experimento: {t_total:.2f} segundos (< 2 minutos exigidos).")
    print("=" * 76)

    # 7. Exportar resumen JSON del experimento
    salida_json = {
        "configuracion": cfg,
        "parametros_entrenables": num_params,
        "epocas_ejecutadas": int(mlp.n_iter_),
        "tiempo_total_segundos": round(t_total, 2),
        "validacion": {
            "AUC": round(auc_val, 4),
            "Gini": round(gini_val, 4),
            "KS": round(ks_val, 4),
            "Brier": round(brier_val, 5),
            "BCE": round(bce_val, 5)
        },
        "prueba": {
            "AUC": round(auc_test, 4),
            "Gini": round(gini_test, 4),
            "KS": round(ks_test, 4),
            "Brier": round(brier_test, 5),
            "BCE": round(bce_test, 5)
        },
        "scorecard": {
            "Factor": round(factor, 4),
            "Offset": round(offset, 4),
            "Score_Mediano_Test": round(float(np.median(scores_test)), 1)
        }
    }
    with open(BASE_DIR / "salida_experimento.json", "w", encoding="utf-8") as f:
        json.dump(salida_json, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
