# -*- coding: utf-8 -*-
"""
Script de exportación de modelos y artefactos para la Aplicación Web
Entregable 2 y 4 - Trabajo 2 Redes Neuronales
"""

import time
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import kagglehub

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neural_network import MLPClassifier, MLPRegressor

# 1. Definición de rutas y directorios
BASE_DIR = Path(__file__).resolve().parent
SALIDA_MODELOS = BASE_DIR / "modelos"
SALIDA_MODELOS.mkdir(exist_ok=True, parents=True)

print(f"Directorio de artefactos: {SALIDA_MODELOS}")

# 2. Configuración de variables y scorecard
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

CAMPOS_LGD = [
    "funded_amnt",
    "total_rec_prncp",
    "recoveries",
    "collection_recovery_fee"
]

# Parámetros oficiales de la Scorecard
S0 = 600.0
ODDS0 = 20.0
PDO = 50.0
FACTOR = PDO / np.log(2)
OFFSET = S0 - FACTOR * np.log(ODDS0)

def prob_a_score(p):
    p = np.asarray(p, dtype=float)
    q = np.where(p <= 0, 1e-12, np.where(p >= 1, 1 - 1e-12, p))
    return OFFSET + FACTOR * (np.log1p(-q) - np.log(q))

# 3. Cargar datos
print("\n--- PASO 1.1: CARGANDO DATASET ---")
t0 = time.time()
archivo_local_procesado = BASE_DIR / "datos" / "base_procesada_cohorte.csv.gz"

if archivo_local_procesado.exists():
    print(f"Cargando dataset local procesado offline: {archivo_local_procesado}")
    cohorte = pd.read_csv(archivo_local_procesado, low_memory=False)
    cohorte["target_pd"] = cohorte["target_pd"].astype(int)
    print(f"Cargadas {len(cohorte):,} filas en {time.time() - t0:.2f} s sin requerir internet.")
else:
    print("Dataset local procesado no encontrado. Descargando/localizando con KaggleHub...")
    dataset_dir = Path(kagglehub.dataset_download("ranadeep/credit-risk-dataset"))
    csv_file = next(dataset_dir.rglob("loan.csv"))
    print(f"Archivo de datos encontrado: {csv_file}")

    columnas_lectura = list(dict.fromkeys(
        ["id", "issue_d", "loan_status", "term", "earliest_cr_line"]
        + [c for c in FEATURES if c != "credit_history_years"]
        + CAMPOS_LGD
    ))

    df = pd.read_csv(csv_file, usecols=columnas_lectura, low_memory=False)
    print(f"Cargadas {len(df):,} filas en {time.time() - t0:.2f} s")

    mapa_pd = {
        "Fully Paid": 0,
        "Does not meet the credit policy. Status:Fully Paid": 0,
        "Charged Off": 1,
        "Default": 1,
        "Late (31-120 days)": 1,
        "Does not meet the credit policy. Status:Charged Off": 1,
    }
    df["target_pd"] = df["loan_status"].map(mapa_pd)
    df["issue_date"] = pd.to_datetime(df["issue_d"], format="%b-%Y")
    df["term_months"] = pd.to_numeric(
        df["term"].astype("string").str.strip().str.replace(" months", "", regex=False),
        errors="coerce"
    )

    mask_cohorte = (
        df["term_months"].eq(36)
        & df["issue_date"].lt("2013-01-01")
        & df["target_pd"].notna()
    )
    cohorte = df.loc[mask_cohorte].copy()
    cohorte["target_pd"] = cohorte["target_pd"].astype(int)

    primera_linea = pd.to_datetime(cohorte["earliest_cr_line"], format="%b-%Y")
    meses = (
        (cohorte["issue_date"].dt.year - primera_linea.dt.year) * 12
        + cohorte["issue_date"].dt.month
        - primera_linea.dt.month
    )
    cohorte["credit_history_years"] = meses / 12.0
    cohorte["revol_util"] = pd.to_numeric(
        cohorte["revol_util"].astype("string").str.strip().str.rstrip("%"),
        errors="coerce"
    )

    cohorte["split"] = "train"
    cohorte.loc[cohorte["issue_date"].ge("2012-01-01"), "split"] = "validation"
    cohorte.loc[cohorte["issue_date"].ge("2012-07-01"), "split"] = "test"

    # Guardar copia procesada offline para cumplir el entregable
    archivo_local_procesado.parent.mkdir(exist_ok=True, parents=True)
    cohorte.to_csv(archivo_local_procesado, index=False, compression="gzip")
    print(f"Copia comprimida guardada en {archivo_local_procesado}")

train = cohorte.loc[cohorte["split"].eq("train")].copy()
val = cohorte.loc[cohorte["split"].eq("validation")].copy()
test = cohorte.loc[cohorte["split"].eq("test")].copy()

print(f"Cohorte total: {len(cohorte):,} créditos")
print(f"Train (2007-2011): {len(train):,} créditos")
print(f"Validation (2012-1): {len(val):,} créditos")
print(f"Test (2012-2): {len(test):,} créditos")

# 5. Ajustar Preprocesador
print("\n--- PASO 1.3: AJUSTE DEL PREPROCESADOR ---")
def preparar_entrada(tabla):
    X = tabla[FEATURES].copy()
    for var in NUMERICAS:
        X[var] = pd.to_numeric(X[var], errors="coerce").astype("float64")
    for var in CATEGORICAS:
        serie = X[var].astype("object")
        X[var] = serie.where(serie.notna(), np.nan)
    return X

X_train_raw = preparar_entrada(train)
X_val_raw = preparar_entrada(val)

preprocesador = ColumnTransformer(
    transformers=[
        (
            "numericas",
            Pipeline([
                ("imputar", SimpleImputer(strategy="median", add_indicator=True)),
                ("escalar", StandardScaler())
            ]),
            NUMERICAS
        ),
        (
            "categoricas",
            Pipeline([
                ("imputar", SimpleImputer(strategy="constant", fill_value="Sin dato")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
            ]),
            CATEGORICAS
        )
    ],
    remainder="drop",
    sparse_threshold=0
)

X_train_trans = np.asarray(preprocesador.fit_transform(X_train_raw), dtype=np.float64)
X_val_trans = np.asarray(preprocesador.transform(X_val_raw), dtype=np.float64)
y_train_pd = train["target_pd"].to_numpy(dtype=np.int64)
y_val_pd = val["target_pd"].to_numpy(dtype=np.int64)

# 6. Entrenar Modelo MLP de Clasificación (PD)
print("\n--- PASO 1.4: ENTRENAMIENTO MLP DE CLASIFICACIÓN (PD) ---")
# Configuración óptima de búsqueda de la Parte 1
mlp_pd = MLPClassifier(
    hidden_layer_sizes=(32, 16),
    activation="relu",
    alpha=0.0001,
    learning_rate_init=0.003,
    solver="adam",
    batch_size=256,
    max_iter=100,
    early_stopping=True,
    n_iter_no_change=8,
    random_state=42
)
mlp_pd.fit(X_train_trans, y_train_pd)
prob_val = mlp_pd.predict_proba(X_val_trans)[:, 1]
print(f"MLP PD entrenado exitosamente. Épocas: {mlp_pd.n_iter_}")

# 7. Entrenar Modelo MLP de Regresión (LGD)
print("\n--- PASO 1.5: ENTRENAMIENTO MLP DE REGRESIÓN (LGD) ---")
# Cálculo de LGD sobre créditos con incumplimiento (target_pd == 1)
def calcular_lgd(df_in):
    monto = pd.to_numeric(df_in["funded_amnt"], errors="coerce")
    rec_prncp = pd.to_numeric(df_in["total_rec_prncp"], errors="coerce").fillna(0)
    rec_bruta = pd.to_numeric(df_in["recoveries"], errors="coerce").fillna(0)
    costo_cobranza = pd.to_numeric(df_in["collection_recovery_fee"], errors="coerce").fillna(0)
    rec_neta = rec_prncp + rec_bruta - costo_cobranza
    lgd_bruta = 1.0 - (rec_neta / monto)
    return np.clip(lgd_bruta, 0.0, 1.0)

train_lgd_sub = train.loc[train["target_pd"].eq(1)].copy()
train_lgd_sub["target_lgd"] = calcular_lgd(train_lgd_sub)
X_train_lgd_trans = preprocesador.transform(preparar_entrada(train_lgd_sub))
y_train_lgd = train_lgd_sub["target_lgd"].to_numpy(dtype=np.float64)

mlp_lgd = MLPRegressor(
    hidden_layer_sizes=(32, 16),
    activation="relu",
    alpha=0.0001,
    learning_rate_init=0.001,
    solver="adam",
    max_iter=100,
    early_stopping=True,
    n_iter_no_change=8,
    random_state=42
)
mlp_lgd.fit(X_train_lgd_trans, y_train_lgd)
print(f"MLP LGD entrenado exitosamente. Épocas: {mlp_lgd.n_iter_}")

# 8. Generar Distribución Poblacional de Puntajes (Scorecard de referencia)
print("\n--- PASO 1.6: GENERANDO DISTRIBUCIÓN POBLACIONAL DE SCORES ---")
prob_train = mlp_pd.predict_proba(X_train_trans)[:, 1]
scores_train = prob_a_score(prob_train)
scores_ordenados = np.sort(scores_train)

# 9. Guardar todos los artefactos en disco
print("\n--- PASO 1.7: SERIALIZANDO ARTEFACTOS ---")
joblib.dump(preprocesador, SALIDA_MODELOS / "preprocesador.joblib")
joblib.dump(mlp_pd, SALIDA_MODELOS / "mlp_pd.joblib")
joblib.dump(mlp_lgd, SALIDA_MODELOS / "mlp_lgd.joblib")

np.savez_compressed(
    SALIDA_MODELOS / "referencia_percentil_train.npz",
    scores_ordenados=scores_ordenados
)

config_scorecard = {
    "S0": S0,
    "ODDS0": ODDS0,
    "PDO": PDO,
    "FACTOR": float(FACTOR),
    "OFFSET": float(OFFSET),
    "NUMERICAS": NUMERICAS,
    "CATEGORICAS": CATEGORICAS,
    "FEATURES": FEATURES,
    "medianas_train": train[NUMERICAS].median().to_dict(),
    "modas_train": {cat: str(train[cat].mode().iloc[0]) for cat in CATEGORICAS}
}

with open(SALIDA_MODELOS / "config_scorecard.json", "w", encoding="utf-8") as f:
    json.dump(config_scorecard, f, indent=2, ensure_ascii=False)

print("\nArtefactos guardados exitosamente:")
for p in SALIDA_MODELOS.glob("*"):
    print(f" - {p.name} ({p.stat().st_size:,} bytes)")

# 10. Prueba de verificación de inferencia
print("\n--- VERIFICACIÓN DE INFERENCIA INMEDIATA ---")
test_user = pd.DataFrame([{
    "loan_amnt": 10000.0,
    "annual_inc": 55000.0,
    "dti": 15.2,
    "delinq_2yrs": 0.0,
    "inq_last_6mths": 1.0,
    "open_acc": 8.0,
    "pub_rec": 0.0,
    "revol_bal": 4500.0,
    "revol_util": 35.0,
    "total_acc": 15.0,
    "credit_history_years": 8.5,
    "emp_length": "5 years",
    "home_ownership": "MORTGAGE",
    "purpose": "debt_consolidation"
}])

user_trans = preprocesador.transform(test_user[FEATURES])
pd_pred = float(mlp_pd.predict_proba(user_trans)[:, 1][0])
lgd_pred = float(np.clip(mlp_lgd.predict(user_trans)[0], 0.0, 1.0))
score_pred = float(prob_a_score(pd_pred))
percentil = float(np.searchsorted(scores_ordenados, score_pred) / len(scores_ordenados) * 100.0)
el_pred = pd_pred * lgd_pred * float(test_user["loan_amnt"].iloc[0])

print(f"Usuario de prueba:")
print(f" -> Probabilidad de Incumplimiento (PD): {pd_pred:.2%}")
print(f" -> Score en la Scorecard: {score_pred:.1f} pts")
print(f" -> Percentil poblacional: {percentil:.1f}%")
print(f" -> Pérdida Dado Incumplimiento (LGD): {lgd_pred:.2%}")
print(f" -> Pérdida Esperada (E[L]): ${el_pred:,.2f}")
print("\n¡PASO 1 COMPLETADO CON ÉXITO!")
