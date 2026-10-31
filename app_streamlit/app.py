# -*- coding: utf-8 -*-
"""
================================================================================
APLICACIÓN WEB: ¿ME PRESTAS? — MOTOR DE EVALUACIÓN PD & SCORECARD
================================================================================
Diseño UI/UX Dark-Tech · Atmósfera Verde Esmeralda & Pizarra con Gradientes
Textos en Español para Destino, Vivienda y Antigüedad Laboral
Semestre 2026-02 · Redes Neuronales y Algoritmos Bioinspirados
Universidad Nacional de Colombia - Facultad de Minas
================================================================================
"""

import time
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import streamlit as st
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y SISTEMA DE DISEÑO DARK-TECH ESMERALDA
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="¿Me prestas? · Scoring Crediticio & Scorecard",
    page_icon="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/shield-check.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS - Atmósfera Verde Esmeralda / Bosque Profundo y Gradientes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: #070B09;
        --bg-surface: #0E1612;
        --bg-surface-elevated: #14201B;
        --bg-input: #0A110E;
        --border-subtle: #192D24;
        --border-wine: rgba(16, 185, 129, 0.35);
        --border-wine-hover: rgba(52, 211, 153, 0.65);
        --text-primary: #F0FDF4;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --wine-deep: #064E3B;
        --wine-glow: rgba(16, 185, 129, 0.22);
        --crimson-accent: #10B981;
        --crimson-button: #059669;
        --cyan-electric: #00D2FF;
        --emerald-tech: #10B981;
        --amber-warning: #F59E0B;
    }

    /* Fondo principal del lienzo con gradiente radial verde esmeralda sutil */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: var(--bg-main) !important;
        background-image: 
            radial-gradient(circle at 88% 8%, rgba(6, 95, 70, 0.28) 0%, rgba(4, 47, 46, 0.14) 42%, transparent 75%),
            radial-gradient(circle at 12% 90%, rgba(5, 150, 105, 0.16) 0%, transparent 60%) !important;
        background-attachment: fixed !important;
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* ==========================================================================
       1. PANEL LATERAL (SIDEBAR): GRADIENTE VERDE BOSQUE PROFUNDO -> PIZARRA
       ========================================================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07100D 0%, #0C1A15 45%, #0B1317 100%) !important;
        border-right: 1px solid var(--border-wine) !important;
        box-shadow: 6px 0 28px rgba(2, 18, 12, 0.55) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }

    .sidebar-header-box {
        padding-bottom: 4px;
        margin-bottom: 18px;
    }
    .sidebar-brand-pill {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #6EE7B7;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .sidebar-app-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #6EE7B7;
        margin: 0 0 2px 0;
        line-height: 1.15;
    }
    .sidebar-main-title {
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.25;
    }
    .sidebar-main-subtitle {
        font-size: 0.76rem;
        color: #86EFAC;
        margin-top: 4px;
        display: block;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ==========================================================================
       2. ENCABEZADOS DE SECCIÓN: VERDE ESMERALDA / BOSQUE PROFUNDO
       ========================================================================== */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: transparent !important;
        border: none !important;
        margin-bottom: 12px !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] > details {
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: rgba(11, 20, 16, 0.94) !important;
        box-shadow: 0 4px 14px rgba(4, 28, 18, 0.3) !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] > details > summary {
        background: linear-gradient(90deg, rgba(6, 78, 59, 0.88) 0%, rgba(4, 47, 46, 0.78) 100%) !important;
        border-bottom: 1px solid rgba(16, 185, 129, 0.3) !important;
        padding: 10px 14px !important;
        color: #ECFDF5 !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] > details > summary:hover {
        background: linear-gradient(90deg, rgba(5, 150, 105, 0.95) 0%, rgba(6, 95, 70, 0.88) 100%) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] > details > summary svg {
        color: #6EE7B7 !important;
        fill: #6EE7B7 !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] > details > div[data-testid="stExpanderDetails"] {
        padding: 14px 14px 8px 14px !important;
        background-color: rgba(10, 19, 15, 0.95) !important;
    }

    /* ==========================================================================
       3. INPUTS Y SELECTORES
       ========================================================================== */
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: rgba(9, 17, 14, 0.95) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.84rem !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stNumberInput input:focus,
    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 1px #10B981 !important;
    }

    /* ==========================================================================
       4. BOTÓN DE ACCIÓN PRINCIPAL (VERDE ESMERALDA / BOSQUE BRILLANTE)
       ========================================================================== */
    [data-testid="stSidebar"] div.stButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.04em !important;
        border: 1px solid #10B981 !important;
        border-radius: 12px !important;
        padding: 13px 20px !important;
        width: 100% !important;
        box-shadow: 0 6px 22px rgba(5, 150, 105, 0.45) !important;
        transition: all 0.15s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-top: 14px !important;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        box-shadow: 0 8px 28px rgba(16, 185, 129, 0.6) !important;
        border-color: #34D399 !important;
        transform: translateY(-1px) !important;
    }

    /* ==========================================================================
       5. LIENZO PRINCIPAL: TARJETAS CON SUTIL GRADIENTE Y BORDE VERDE ESMERALDA
       ========================================================================== */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border-wine);
        margin-bottom: 20px;
    }
    .app-brand-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        color: #6EE7B7;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .header-main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #6EE7B7;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin: 0 0 4px 0;
    }
    .header-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.01em;
        margin: 0 0 4px 0;
    }
    .header-subtitle {
        font-size: 0.82rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
    }
    .nav-actions {
        display: flex;
        gap: 8px;
    }
    .nav-btn {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        color: var(--text-secondary);
        background: linear-gradient(145deg, #0F1714 0%, #13221C 100%);
        border: 1px solid var(--border-wine);
        padding: 6px 12px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.15s ease;
    }
    .nav-btn:hover {
        color: #FFFFFF;
        border-color: var(--border-wine-hover);
        background: #14251E;
        text-decoration: none;
    }
    .nav-btn svg {
        width: 13px;
        height: 13px;
        stroke: currentColor;
    }

    /* Tarjetas KPI con Gradiente Pizarra-Verde Esmeralda */
    .kpi-card {
        background: linear-gradient(145deg, #0F1714 0%, #14231D 100%);
        border: 1px solid var(--border-wine);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 18px rgba(4, 25, 17, 0.4);
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .kpi-card:hover {
        border-color: var(--border-wine-hover);
    }
    .kpi-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text-muted);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kpi-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Estado de espera / Empty State con resplandor sutil */
    .empty-state-panel {
        background: linear-gradient(145deg, #0E1612 0%, #13221B 100%);
        border: 1px dashed var(--border-wine);
        border-radius: 16px;
        padding: 56px 32px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 8px 30px rgba(4, 25, 17, 0.45);
    }
    .empty-state-icon {
        width: 44px;
        height: 44px;
        stroke: #10B981;
        margin: 0 auto 16px;
        display: block;
        opacity: 0.9;
    }
    .empty-state-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    .empty-state-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        max-width: 540px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Panel de Diagnóstico con Acento Lateral */
    .diagnosis-container {
        background: linear-gradient(145deg, #0F1714 0%, #14231D 100%);
        border: 1px solid var(--border-wine);
        border-radius: 12px;
        padding: 20px 24px;
        margin-top: 20px;
        box-shadow: 0 4px 18px rgba(4, 25, 17, 0.4);
    }
    .diagnosis-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .diagnosis-body {
        font-size: 0.9rem;
        line-height: 1.6;
        color: var(--text-secondary);
    }

    /* Tabs Segmentados con Borde Verde Esmeralda */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(11, 20, 16, 0.9) !important;
        border: 1px solid var(--border-wine) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        margin-bottom: 24px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        transition: all 0.15s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.85) 0%, rgba(4, 47, 46, 0.95) 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.5) !important;
    }

    .percentile-track {
        width: 100%;
        height: 4px;
        background: #2A2F3A;
        border-radius: 2px;
        margin-top: 6px;
        overflow: hidden;
    }
    .percentile-fill {
        height: 100%;
        border-radius: 2px;
        background: var(--cyan-electric);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. CARGA DE MODELOS Y DICCIONARIOS DE TRADUCCIÓN A ESPAÑOL
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR if (BASE_DIR / "modelos").exists() else BASE_DIR.parent
MODEL_DIR = ROOT_DIR / "modelos"

# Mapeos Amigables en Español -> Valores de Entrada al Modelo
MAPA_PROPOSITO = {
    "Consolidación de deudas": "debt_consolidation",
    "Tarjetas de crédito / Refinanciación": "credit_card",
    "Mejoras y reformas del hogar": "home_improvement",
    "Compras mayores / Bienes durables": "major_purchase",
    "Pequeño negocio / Emprendimiento": "small_business",
    "Compra de vehículo": "car",
    "Gastos médicos y salud": "medical",
    "Boda y eventos familiares": "wedding",
    "Mudanza y reubicación": "moving",
    "Vacaciones y viajes": "vacation",
    "Compra o remodelación de vivienda": "house",
    "Otro propósito": "other"
}
MAPA_PROPOSITO_INV = {v: k for k, v in MAPA_PROPOSITO.items()}

MAPA_VIVIENDA = {
    "Hipoteca vigente (Vivienda financiada)": "MORTGAGE",
    "Arrendamiento / Alquiler": "RENT",
    "Vivienda propia (Pagada)": "OWN",
    "Otro régimen de vivienda": "OTHER"
}
MAPA_VIVIENDA_INV = {v: k for k, v in MAPA_VIVIENDA.items()}

MAPA_ANTIGUEDAD = {
    "Menos de 1 año": "< 1 year",
    "1 año": "1 year",
    "2 años": "2 years",
    "3 años": "3 years",
    "4 años": "4 years",
    "5 años": "5 years",
    "6 años": "6 years",
    "7 años": "7 years",
    "8 años": "8 years",
    "9 años": "9 years",
    "10 o más años": "10+ years",
    "Sin registro / No especificado": "Sin dato"
}
MAPA_ANTIGUEDAD_INV = {v: k for k, v in MAPA_ANTIGUEDAD.items()}

@st.cache_resource
def cargar_artefactos():
    try:
        preprocesador = joblib.load(MODEL_DIR / "preprocesador.joblib")
        mlp_pd = joblib.load(MODEL_DIR / "mlp_pd.joblib")
        mlp_lgd = joblib.load(MODEL_DIR / "mlp_lgd.joblib")
        datos_npz = np.load(MODEL_DIR / "referencia_percentil_train.npz")
        scores_referencia = datos_npz["scores_ordenados"]
        
        with open(MODEL_DIR / "config_scorecard.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            
        return {
            "preprocesador": preprocesador,
            "mlp_pd": mlp_pd,
            "mlp_lgd": mlp_lgd,
            "scores_referencia": scores_referencia,
            "config": config,
            "exito": True
        }
    except Exception as e:
        return {"exito": False, "error": str(e)}

artefactos = cargar_artefactos()

if not artefactos["exito"]:
    st.error(f"Error cargando modelos desde '{MODEL_DIR}': {artefactos['error']}")
    st.info("Ejecuta primero: python exportar_artefactos.py")

    with st.expander("🎬 Reproducir Video Promocional y Sustentaciones del Equipo", expanded=True):
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.76rem; color:#FCA5A5; text-transform:uppercase; margin-bottom:8px; font-weight:700;">
            PITCH OFICIAL · PLATAFORMA FINTECH ¿ME PRESTAS?
        </div>
        """, unsafe_allow_html=True)
        col_vid_promo, col_vid_info = st.columns([3, 2])
        with col_vid_promo:
            st.video("https://youtu.be/lFPKU94AXQw")
        with col_vid_info:
            st.markdown("""
            <div style="padding:14px; background:rgba(0,0,0,0.3); border-radius:8px; border:1px solid rgba(136,19,35,0.35);">
                <div style="font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:6px;">¿Me prestas? — Solución Integral</div>
                <div style="font-size:0.78rem; color:#94A3B8; line-height:1.5; margin-bottom:12px;">
                    Video promocional de 2 a 3 minutos presentando la aplicación web como motor de decisión crediticia y cálculo de provisiones esperadas bajo Basilea II/III.
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.73rem; color:#00D2FF; font-weight:700; margin-bottom:6px;">VIDEOS INDIVIDUALES:</div>
                <ul style="list-style:none; padding-left:0; margin:0; font-size:0.75rem; line-height:1.9;">
                    <li><a href="https://www.youtube.com/watch?v=8MujIkYyee8" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">David Agudelo:</b> Despliegue Streamlit & What-If ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=m8Ez_CVvfpY" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Alejandro Agudelo:</b> Calibración & Cacería IA ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=9hN8B1hWywM" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Daniel López:</b> Clasificador MLP & PD ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=64bk3zrYsFU" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Sara Osorio:</b> Modelado LGD & Pérdida Esperada ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=lRHa541LBnY" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Santiago Álvarez (Baco):</b> Datos & Cohorte ↗</a></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.stop()

preprocesador = artefactos["preprocesador"]
mlp_pd = artefactos["mlp_pd"]
mlp_lgd = artefactos["mlp_lgd"]
scores_referencia = artefactos["scores_referencia"]
config = artefactos["config"]

OFFSET = config["OFFSET"]
FACTOR = config["FACTOR"]
FEATURES = config["FEATURES"]
NUMERICAS = config["NUMERICAS"]
CATEGORICAS = config["CATEGORICAS"]

def prob_a_score(p):
    p = np.asarray(p, dtype=float)
    q = np.where(p <= 0, 1e-12, np.where(p >= 1, 1 - 1e-12, p))
    return OFFSET + FACTOR * (np.log1p(-q) - np.log(q))

def score_a_prob(s):
    return 1.0 / (1.0 + np.exp((OFFSET - s) / FACTOR))

def calcular_percentil(score_val):
    idx = np.searchsorted(scores_referencia, score_val)
    return (idx / len(scores_referencia)) * 100.0

if "ejecutado" not in st.session_state:
    st.session_state["ejecutado"] = False

# ------------------------------------------------------------------------------
# 3. BARRA SUPERIOR Y NAVEGACIÓN
# ------------------------------------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <div>
        <div class="app-brand-badge">PLATAFORMA FINTECH INTELIGENTE</div>
        <h1 class="header-main-title">¿Me prestas?</h1>
        <div class="header-title">Scoring Crediticio · Motor de Evaluación PD & Scorecard</div>
        <div class="header-subtitle">Modelo de Redes Neuronales Artificiales (MLP) · Lending Club Dataset</div>
    </div>
    <div class="nav-actions">
        <a class="nav-btn" href="https://davidagr5421.github.io/Trabajo02RedesNeuronales/" target="_blank">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Reporte Blog
        </a>
        <a class="nav-btn" href="https://youtu.be/lFPKU94AXQw" target="_blank">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
            Video Demo
        </a>
        <a class="nav-btn" href="https://github.com/DavidAgr5421/Trabajo02RedesNeuronales" target="_blank">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
            GitHub
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. BARRA LATERAL IZQUIERDA: "PARÁMETROS DEL SOLICITANTE"
# ------------------------------------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-header-box">
    <div class="sidebar-brand-pill">PLATAFORMA FINTECH</div>
    <div class="sidebar-app-title">¿Me prestas?</div>
    <div class="sidebar-main-title">Parámetros del Solicitante</div>
    <span class="sidebar-main-subtitle">Configura los atributos contractuales y crediticios</span>
</div>
""", unsafe_allow_html=True)

perfil = st.sidebar.selectbox(
    "Perfil de demostración:",
    ["Personalizado", "Perfil A: Riesgo Bajo (Excelente)", "Perfil B: Riesgo Moderado (Promedio)", "Perfil C: Riesgo Alto (Crítico)"]
)

# Parámetros predefinidos por perfil (con claves en inglés para el backend)
if perfil == "Perfil A: Riesgo Bajo (Excelente)":
    def_loan = 7500.0; def_inc = 94000.0; def_dti = 8.5; def_delinq = 0; def_inq = 0
    def_open = 11; def_pub = 0; def_bal = 3100.0; def_util = 16.0; def_total = 24; def_hist = 15.0
    def_emp_raw = "10+ years"; def_home_raw = "MORTGAGE"; def_purpose_raw = "credit_card"
elif perfil == "Perfil C: Riesgo Alto (Crítico)":
    def_loan = 26000.0; def_inc = 31000.0; def_dti = 29.5; def_delinq = 2; def_inq = 4
    def_open = 5; def_pub = 1; def_bal = 19500.0; def_util = 95.0; def_total = 9; def_hist = 3.0
    def_emp_raw = "< 1 year"; def_home_raw = "RENT"; def_purpose_raw = "small_business"
else:
    def_loan = 12000.0; def_inc = 54000.0; def_dti = 16.5; def_delinq = 0; def_inq = 1
    def_open = 8; def_pub = 0; def_bal = 8200.0; def_util = 48.0; def_total = 18; def_hist = 8.5
    def_emp_raw = "5 years"; def_home_raw = "RENT"; def_purpose_raw = "debt_consolidation"

lista_propositos_es = list(MAPA_PROPOSITO.keys())
lista_vivienda_es = list(MAPA_VIVIENDA.keys())
lista_antiguedad_es = list(MAPA_ANTIGUEDAD.keys())

with st.sidebar.expander("01. Condiciones del Crédito", expanded=True):
    loan_amnt = st.number_input("Monto solicitado (USD):", min_value=500.0, max_value=40000.0, value=float(def_loan), step=500.0)
    proposito_sel_es = st.selectbox(
        "Destino del financiamiento:",
        lista_propositos_es,
        index=lista_propositos_es.index(MAPA_PROPOSITO_INV[def_purpose_raw])
    )
    purpose_model = MAPA_PROPOSITO[proposito_sel_es]

with st.sidebar.expander("02. Capacidad Financiera (DTI & Ingresos)", expanded=True):
    annual_inc = st.number_input("Ingreso anual verificado (USD):", min_value=4000.0, max_value=600000.0, value=float(def_inc), step=2500.0)
    dti = st.slider("Relación Deuda/Ingreso - DTI (%):", min_value=0.0, max_value=40.0, value=float(def_dti), step=0.5)
    
    antiguedad_sel_es = st.selectbox(
        "Antigüedad laboral:",
        lista_antiguedad_es,
        index=lista_antiguedad_es.index(MAPA_ANTIGUEDAD_INV[def_emp_raw])
    )
    emp_length_model = MAPA_ANTIGUEDAD[antiguedad_sel_es]

    vivienda_sel_es = st.selectbox(
        "Régimen de vivienda:",
        lista_vivienda_es,
        index=lista_vivienda_es.index(MAPA_VIVIENDA_INV[def_home_raw])
    )
    home_ownership_model = MAPA_VIVIENDA[vivienda_sel_es]

with st.sidebar.expander("03. Historial Crediticio", expanded=False):
    credit_history_years = st.slider("Años de historial:", min_value=1.0, max_value=40.0, value=float(def_hist), step=0.5)
    revol_util = st.slider("Uso de crédito rotativo (%):", min_value=0.0, max_value=120.0, value=float(def_util), step=1.0)
    revol_bal = st.number_input("Saldo en tarjetas de crédito (USD):", min_value=0.0, max_value=250000.0, value=float(def_bal), step=500.0)
    inq_last_6mths = st.number_input("Consultas en últimos 6 meses:", min_value=0, max_value=15, value=int(def_inq))
    delinq_2yrs = st.number_input("Moras de 30+ días (últimos 2 años):", min_value=0, max_value=15, value=int(def_delinq))
    pub_rec = st.number_input("Registros públicos desfavorables:", min_value=0, max_value=10, value=int(def_pub))
    open_acc = st.number_input("Cuentas de crédito abiertas:", min_value=1, max_value=50, value=int(def_open))
    total_acc = st.number_input("Total de cuentas históricas:", min_value=1, max_value=100, value=int(def_total))


with st.sidebar.expander("🎬 Videos del Proyecto", expanded=True):
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.74rem; color:#FCA5A5; text-transform:uppercase; margin-bottom:8px; font-weight:700;">
        PITCH & SUSTENTACIÓN TÉCNICA
    </div>
    <a href="https://youtu.be/lFPKU94AXQw" target="_blank" style="display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(90deg, #DC2626 0%, #B91C1C 100%); color:#FFFFFF; padding:10px 14px; border-radius:8px; font-weight:700; font-size:0.8rem; text-decoration:none; margin-bottom:12px; box-shadow:0 4px 12px rgba(220,38,38,0.35);">
        ▶ Video Promocional (Pitch) ↗
    </a>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#94A3B8; margin-bottom:6px; font-weight:600;">VIDEOS INDIVIDUALES:</div>
    <div style="display:flex; flex-direction:column; gap:5px;">
        <a href="https://www.youtube.com/watch?v=8MujIkYyee8" target="_blank" style="display:flex; justify-content:space-between; align-items:center; padding:6px 9px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; color:#F8FAFC; text-decoration:none; font-size:0.74rem;">
            <span><b style="color:#00D2FF;">David Agudelo:</b> App & What-if</span>
            <span style="color:#94A3B8;">↗</span>
        </a>
        <a href="https://www.youtube.com/watch?v=m8Ez_CVvfpY" target="_blank" style="display:flex; justify-content:space-between; align-items:center; padding:6px 9px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; color:#F8FAFC; text-decoration:none; font-size:0.74rem;">
            <span><b style="color:#00D2FF;">Alejandro Agudelo:</b> Calibración</span>
            <span style="color:#94A3B8;">↗</span>
        </a>
        <a href="https://www.youtube.com/watch?v=9hN8B1hWywM" target="_blank" style="display:flex; justify-content:space-between; align-items:center; padding:6px 9px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; color:#F8FAFC; text-decoration:none; font-size:0.74rem;">
            <span><b style="color:#00D2FF;">Daniel López:</b> MLP & PD</span>
            <span style="color:#94A3B8;">↗</span>
        </a>
        <a href="https://www.youtube.com/watch?v=64bk3zrYsFU" target="_blank" style="display:flex; justify-content:space-between; align-items:center; padding:6px 9px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; color:#F8FAFC; text-decoration:none; font-size:0.74rem;">
            <span><b style="color:#00D2FF;">Sara Osorio:</b> Regresión LGD</span>
            <span style="color:#94A3B8;">↗</span>
        </a>
        <a href="https://www.youtube.com/watch?v=lRHa541LBnY" target="_blank" style="display:flex; justify-content:space-between; align-items:center; padding:6px 9px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:6px; color:#F8FAFC; text-decoration:none; font-size:0.74rem;">
            <span><b style="color:#00D2FF;">Santiago (Baco):</b> EDA & Datos</span>
            <span style="color:#94A3B8;">↗</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Botón Principal CTA: "Calcular Riesgo Crediticio" (Verde Esmeralda Tech)
btn_evaluar = st.sidebar.button("Calcular Riesgo Crediticio")

if btn_evaluar:
    with st.spinner("Procesando inferencia del modelo MLP..."):
        time.sleep(0.3)
        st.session_state["ejecutado"] = True

# ------------------------------------------------------------------------------
# 5. ESTADO INICIAL (PRE-CÁLCULO)
# ------------------------------------------------------------------------------
if not st.session_state["ejecutado"]:
    st.markdown("""
    <div class="empty-state-panel">
        <svg class="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <line x1="8" y1="21" x2="16" y2="21"></line>
            <line x1="12" y1="17" x2="12" y2="21"></line>
        </svg>
        <div class="empty-state-title">Motor de Evaluación en Espera</div>
        <div class="empty-state-desc">
            Ingresa o ajusta los parámetros del solicitante y presiona <b>'Calcular Riesgo Crediticio'</b> 
            para ejecutar el modelo de inferencia MLP y revelar las métricas analíticas.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_pre1, col_pre2, col_pre3 = st.columns(3)
    with col_pre1:
        st.markdown("""
        <div class="kpi-card" style="margin-top: 16px;">
            <div class="kpi-header">CLASIFICACIÓN BINARIA</div>
            <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">Probabilidad de Impago (PD)</div>
            <div style="font-size: 0.8rem; color: #64748B;">Perceptrón Multicapa optimizado con Binary Cross-Entropy Loss.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_pre2:
        st.markdown("""
        <div class="kpi-card" style="margin-top: 16px;">
            <div class="kpi-header">CALIBRACIÓN SCORECARD</div>
            <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">Escala Oficial SAS</div>
            <div style="font-size: 0.8rem; color: #64748B;">Transformación de log-odds con puntaje base S0=600 @ Odds 20:1 y PDO=50.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_pre3:
        st.markdown("""
        <div class="kpi-card" style="margin-top: 16px;">
            <div class="kpi-header">MODELO DE REGRESIÓN</div>
            <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">Pérdida Esperada (E[L])</div>
            <div style="font-size: 0.8rem; color: #64748B;">Integración E[L] = PD · LGD · EAD con MLPRegressor sobre créditos castigados.</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🎬 Reproducir Video Promocional y Sustentaciones del Equipo", expanded=True):
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.76rem; color:#FCA5A5; text-transform:uppercase; margin-bottom:8px; font-weight:700;">
            PITCH OFICIAL · PLATAFORMA FINTECH ¿ME PRESTAS?
        </div>
        """, unsafe_allow_html=True)
        col_vid_promo, col_vid_info = st.columns([3, 2])
        with col_vid_promo:
            st.video("https://youtu.be/lFPKU94AXQw")
        with col_vid_info:
            st.markdown("""
            <div style="padding:14px; background:rgba(0,0,0,0.3); border-radius:8px; border:1px solid rgba(136,19,35,0.35);">
                <div style="font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:6px;">¿Me prestas? — Solución Integral</div>
                <div style="font-size:0.78rem; color:#94A3B8; line-height:1.5; margin-bottom:12px;">
                    Video promocional de 2 a 3 minutos presentando la aplicación web como motor de decisión crediticia y cálculo de provisiones esperadas bajo Basilea II/III.
                </div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.73rem; color:#00D2FF; font-weight:700; margin-bottom:6px;">VIDEOS INDIVIDUALES:</div>
                <ul style="list-style:none; padding-left:0; margin:0; font-size:0.75rem; line-height:1.9;">
                    <li><a href="https://www.youtube.com/watch?v=8MujIkYyee8" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">David Agudelo:</b> Despliegue Streamlit & What-If ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=m8Ez_CVvfpY" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Alejandro Agudelo:</b> Calibración & Cacería IA ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=9hN8B1hWywM" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Daniel López:</b> Clasificador MLP & PD ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=64bk3zrYsFU" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Sara Osorio:</b> Modelado LGD & Pérdida Esperada ↗</a></li>
                    <li><a href="https://www.youtube.com/watch?v=lRHa541LBnY" target="_blank" style="color:#F8FAFC; text-decoration:none;">▶ <b style="color:#00D2FF;">Santiago Álvarez (Baco):</b> Datos & Cohorte ↗</a></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.stop()

# ------------------------------------------------------------------------------
# 6. INFERENCIA DEL MODELO (ALIMENTADO CON VALORES ORIGINALES MAPEADOS)
# ------------------------------------------------------------------------------
datos_cliente = pd.DataFrame([{
    "loan_amnt": loan_amnt,
    "annual_inc": annual_inc,
    "dti": dti,
    "delinq_2yrs": float(delinq_2yrs),
    "inq_last_6mths": float(inq_last_6mths),
    "open_acc": float(open_acc),
    "pub_rec": float(pub_rec),
    "revol_bal": revol_bal,
    "revol_util": revol_util,
    "total_acc": float(total_acc),
    "credit_history_years": credit_history_years,
    "emp_length": emp_length_model,
    "home_ownership": home_ownership_model,
    "purpose": purpose_model
}])

X_trans = preprocesador.transform(datos_cliente[FEATURES])
pd_estimada = float(mlp_pd.predict_proba(X_trans)[:, 1][0])
lgd_estimada = float(np.clip(mlp_lgd.predict(X_trans)[0], 0.0, 1.0))
score_actual = float(prob_a_score(pd_estimada))
percentil_actual = float(calcular_percentil(score_actual))
perdida_esperada = pd_estimada * lgd_estimada * loan_amnt

if score_actual >= 620:
    dictamen_texto = "Riesgo Bajo · Aprobación Sugerida"
    dictamen_color = "#10B981"
    dictamen_prosa = f"Puntaje favorable ({score_actual:.1f} pts). El perfil presenta solvencia crediticia superior a la mediana del portafolio (Percentil {percentil_actual:.1f}%). La exposición de ${loan_amnt:,.2f} USD califica para desembolso preferencial con pérdida esperada mínima de ${perdida_esperada:,.2f} USD."
elif score_actual >= 520:
    dictamen_texto = "Riesgo Moderado · Revisión Manual"
    dictamen_color = "#F59E0B"
    dictamen_prosa = f"Puntaje moderado ({score_actual:.1f} pts). La probabilidad de incumplimiento ({pd_estimada:.2%}) se ubica en el rango medio del portafolio. Se aconseja solicitar avales complementarios o ajustar el plazo de amortización antes de liquidar el desembolso."
else:
    dictamen_texto = "Riesgo Alto · Exposición Crítica"
    dictamen_color = "#EF4444"
    dictamen_prosa = f"Puntaje de alto riesgo ({score_actual:.1f} pts). El perfil proyecta una probabilidad de incumplimiento crítica ({pd_estimada:.2%}), superando únicamente al {percentil_actual:.1f}% de la población histórica. Se desaconseja la aprobación directa sin mitigantes de liquidez."

# ------------------------------------------------------------------------------
# 7. SUITE ANALÍTICA REVELADA
# ------------------------------------------------------------------------------
tab_diag, tab_whatif, tab_pop, tab_spec, tab_videos = st.tabs([
    "Diagnóstico del Solicitante",
    "Simulador de Impacto (What-if)",
    "Ubicación Poblacional",
    "Metodología del Modelo",
    "🎬 Videos & Sustentación"
])

# --- TAB 1: DIAGNÓSTICO ---
with tab_diag:
    k1, k2, k3, k4 = st.columns(4)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <span>SCORE OFICIAL</span>
                <span style="color: {dictamen_color};">●</span>
            </div>
            <div class="kpi-number" style="color: #FFFFFF;">{score_actual:.1f} <span style="font-size:0.95rem; font-weight:500; color:#64748B;">pts</span></div>
            <div class="kpi-subtext" style="color: {dictamen_color}; font-weight:600;">
                ● {dictamen_texto}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">PROBABILIDAD INCUMPLIMIENTO</div>
            <div class="kpi-number" style="color: var(--cyan-electric);">{pd_estimada:.2%}</div>
            <div class="kpi-subtext">Modelo MLP Classifier</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">PERCENTIL POBLACIONAL</div>
            <div class="kpi-number" style="color: #E2E8F0;">{percentil_actual:.1f}%</div>
            <div class="percentile-track">
                <div class="percentile-fill" style="width: {percentil_actual:.1f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">PÉRDIDA ESPERADA (EL)</div>
            <div class="kpi-number" style="color: #F8FAFC;">${perdida_esperada:,.2f} <span style="font-size:0.85rem; font-weight:500; color:#64748B;">USD</span></div>
            <div class="kpi-subtext">LGD estimada: {lgd_estimada:.1%}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_gauge, col_diag_text = st.columns([3, 2])

    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score_actual,
            number={'suffix': " pts", 'font': {'size': 34, 'family': "JetBrains Mono, monospace", 'color': "#FFFFFF"}},
            title={'text': "<span style='font-family: JetBrains Mono; font-size:0.75rem; color:#94A3B8; letter-spacing:0.08em;'>ESCALA DE CALIFICACIÓN (350 - 750 PTS)</span>"},
            gauge={
                'axis': {'range': [350, 750], 'tickwidth': 1, 'tickcolor': "#1E3A2F", 'tickfont': {'color': "#94A3B8", 'family': "JetBrains Mono", 'size': 10}},
                'bar': {'color': dictamen_color, 'thickness': 0.28},
                'bgcolor': "#141720",
                'borderwidth': 1,
                'bordercolor': "rgba(16, 185, 129, 0.35)",
                'steps': [
                    {'range': [350, 520], 'color': 'rgba(220, 38, 38, 0.25)'},
                    {'range': [520, 620], 'color': 'rgba(245, 158, 11, 0.25)'},
                    {'range': [620, 750], 'color': 'rgba(16, 185, 129, 0.25)'}
                ],
                'threshold': {
                    'line': {'color': "#00D2FF", 'width': 3},
                    'thickness': 0.82,
                    'value': score_actual
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=300,
            margin=dict(l=20, r=20, t=30, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_diag_text:
        st.markdown(f"""
        <div class="diagnosis-container" style="border-left: 3px solid {dictamen_color};">
            <div class="diagnosis-header" style="color: {dictamen_color};">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="{dictamen_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
                DIAGNÓSTICO AUTOMATIZADO
            </div>
            <div class="diagnosis-body">
                {dictamen_prosa}
            </div>
            <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(16, 185, 129, 0.25); font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">
                STATUS: <span style="color: {dictamen_color}; font-weight: 700;">{dictamen_texto.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: SIMULADOR WHAT-IF ---
with tab_whatif:
    st.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #6EE7B7; text-transform: uppercase; margin-bottom: 4px;">
        ANÁLISIS DE SENSIBILIDAD DINÁMICO
    </div>
    <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 20px;">
        Modifica variables financieras accionables para cuantificar el efecto marginal sobre la probabilidad de impago y el puntaje.
    </div>
    """, unsafe_allow_html=True)

    c_w1, c_w2 = st.columns([2, 3])

    with c_w1:
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#F8FAFC; margin-bottom:12px; font-family:JetBrains Mono;'>PARÁMETROS EXPERIMENTALES</div>", unsafe_allow_html=True)
        
        sim_revol_util = st.slider("Uso de crédito rotativo (%):", min_value=0.0, max_value=120.0, value=float(revol_util), step=1.0)
        sim_dti = st.slider("Relación Deuda/Ingreso - DTI (%):", min_value=0.0, max_value=40.0, value=float(dti), step=0.5)
        delta_inc = st.slider("Incremento salarial anual (USD):", min_value=0.0, max_value=60000.0, value=0.0, step=2500.0)
        sim_annual_inc = annual_inc + delta_inc
        sim_inq = st.slider("Consultas recientes de crédito:", min_value=0, max_value=10, value=int(inq_last_6mths), step=1)

    cliente_sim = datos_cliente.copy()
    cliente_sim["revol_util"] = sim_revol_util
    cliente_sim["dti"] = sim_dti
    cliente_sim["annual_inc"] = sim_annual_inc
    cliente_sim["inq_last_6mths"] = float(sim_inq)

    X_sim = preprocesador.transform(cliente_sim[FEATURES])
    pd_sim = float(mlp_pd.predict_proba(X_sim)[:, 1][0])
    score_sim = float(prob_a_score(pd_sim))
    percentil_sim = float(calcular_percentil(score_sim))

    diff_score = score_sim - score_actual
    diff_pd = (pd_sim - pd_estimada) * 100.0
    diff_perc = percentil_sim - percentil_actual

    with c_w2:
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#F8FAFC; margin-bottom:12px; font-family:JetBrains Mono;'>COMPARATIVA MARGINAL: ACTUAL vs. SIMULADO</div>", unsafe_allow_html=True)
        
        cw1, cw2, cw3 = st.columns(3)
        with cw1:
            c_delta = "#10B981" if diff_score >= 0 else "#EF4444"
            st.markdown(f"""
            <div class="kpi-card" style="padding: 16px;">
                <div class="kpi-header">SCORECARD SIMULADA</div>
                <div class="kpi-number" style="font-size: 1.6rem;">{score_sim:.1f}</div>
                <div style="font-family:'JetBrains Mono'; font-size:0.8rem; color:{c_delta}; font-weight:700;">
                    {diff_score:+.1f} pts
                </div>
            </div>
            """, unsafe_allow_html=True)

        with cw2:
            c_delta_pd = "#10B981" if diff_pd <= 0 else "#EF4444"
            st.markdown(f"""
            <div class="kpi-card" style="padding: 16px;">
                <div class="kpi-header">PD SIMULADA</div>
                <div class="kpi-number" style="font-size: 1.6rem; color:var(--cyan-electric);">{pd_sim:.2%}</div>
                <div style="font-family:'JetBrains Mono'; font-size:0.8rem; color:{c_delta_pd}; font-weight:700;">
                    {diff_pd:+.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with cw3:
            c_delta_p = "#00D2FF" if diff_perc >= 0 else "#EF4444"
            st.markdown(f"""
            <div class="kpi-card" style="padding: 16px;">
                <div class="kpi-header">PERCENTIL SIMULADO</div>
                <div class="kpi-number" style="font-size: 1.6rem; color:#E2E8F0;">{percentil_sim:.1f}%</div>
                <div style="font-family:'JetBrains Mono'; font-size:0.8rem; color:{c_delta_p}; font-weight:700;">
                    {diff_perc:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        fig_barras = go.Figure()
        fig_barras.add_trace(go.Bar(
            y=["Puntaje Score", "Percentil (%)"],
            x=[score_actual, percentil_actual],
            name="Estado Base",
            orientation='h',
            marker=dict(color='#11221B', line=dict(color='rgba(16, 185, 129, 0.35)', width=1))
        ))
        fig_barras.add_trace(go.Bar(
            y=["Puntaje Score", "Percentil (%)"],
            x=[score_sim, percentil_sim],
            name="Escenario Simulado",
            orientation='h',
            marker=dict(color='#00D2FF', line=dict(color='#00B8E6', width=1))
        ))
        fig_barras.update_layout(
            barmode='group',
            height=210,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono, monospace", color="#94A3B8", size=10),
            xaxis=dict(showgrid=True, gridcolor="#162E24"),
            yaxis=dict(showgrid=False),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_barras, use_container_width=True)

# --- TAB 3: UBICACIÓN POBLACIONAL ---
with tab_pop:
    st.markdown(f"""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #6EE7B7; text-transform: uppercase; margin-bottom: 4px;">
        DISTRIBUCIÓN HISTÓRICA DEL PORTAFOLIO ({len(scores_referencia):,} CRÉDITOS EN ENTRENAMIENTO)
    </div>
    <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 20px;">
        Curva de densidad probabilística de la base Lending Club. Ubicación del solicitante marcada en <span style="color:{dictamen_color}; font-weight:700;">{score_actual:.1f} pts (Percentil {percentil_actual:.1f}%)</span>.
    </div>
    """, unsafe_allow_html=True)

    hist_vals, bin_edges = np.histogram(scores_referencia, bins=70, density=True)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    fig_densidad = go.Figure()
    fig_densidad.add_trace(go.Scatter(
        x=bin_centers,
        y=hist_vals,
        mode='lines',
        fill='tozeroy',
        name='Densidad Portafolio',
        line=dict(color='#00D2FF', width=2),
        fillcolor='rgba(0, 210, 255, 0.08)'
    ))
    fig_densidad.add_vline(
        x=score_actual,
        line_width=2,
        line_dash="dot",
        line_color=dictamen_color,
        annotation_text=f"SOLICITANTE: {score_actual:.1f} pts (P{percentil_actual:.0f})",
        annotation_position="top right",
        annotation_font=dict(color=dictamen_color, size=11, family="JetBrains Mono")
    )

    fig_densidad.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace", color="#94A3B8", size=10),
        xaxis=dict(title="Puntaje Scorecard (pts)", showgrid=True, gridcolor="#162E24", zeroline=False),
        yaxis=dict(title="Densidad", showgrid=True, gridcolor="#162E24", zeroline=False),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified"
    )
    st.plotly_chart(fig_densidad, use_container_width=True)

    cp1, cp2, cp3 = st.columns(3)
    cp1.metric("Percentil acumulado inferior", f"{percentil_actual:.1f}%")
    cp2.metric("Población con menor riesgo", f"{100.0 - percentil_actual:.1f}%")
    cp3.metric("Mediana histórica del portafolio", f"{np.median(scores_referencia):.1f} pts")

# --- TAB 4: METODOLOGÍA DEL MODELO ---
with tab_spec:
    st.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #6EE7B7; text-transform: uppercase; margin-bottom: 12px;">
        FORMULACIÓN MATEMÁTICA Y ESPECIFICACIÓN DE MODELOS
    </div>
    """, unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#FFFFFF;'>1. Transformación de la Scorecard</div>", unsafe_allow_html=True)
        st.latex(r"S = \text{Offset} + \text{Factor} \cdot \ln\left(\frac{1 - p}{p}\right)")
        st.markdown(f"""
        ```text
        Parámetros fijados:
        S0 (Puntaje base):        {config['S0']} pts
        Odds0 (Odds referencia):   {config['ODDS0']}:1
        PDO (Puntos duplicación):  {config['PDO']} pts
        Factor:                    {FACTOR:.4f}
        Offset:                    {OFFSET:.4f}
        ```
        """)

    with col_m2:
        st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#FFFFFF;'>2. Pérdida Esperada de Crédito</div>", unsafe_allow_html=True)
        st.latex(r"\mathbb{E}[L] = \text{PD} \times \text{LGD} \times \text{EAD}")
        st.markdown("""
        ```text
        PD:  Multi-Layer Perceptron (Salida Logística / BCE)
        LGD: Multi-Layer Perceptron Regressor acotado en [0, 1]
        EAD: Exposición total al incumplimiento (loan_amnt)
        ```
        """)

    st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#FFFFFF; margin-top:16px;'>3. Arquitectura del Perceptrón Multicapa (MLP)</div>", unsafe_allow_html=True)
    st.json({
        "Clasificador PD (MLPClassifier)": {
            "Capas Ocultas": mlp_pd.hidden_layer_sizes,
            "Activación Oculta": mlp_pd.activation,
            "Optimizador": mlp_pd.solver,
            "Tasa de Aprendizaje Inicial": mlp_pd.learning_rate_init,
            "Regularización L2 (alpha)": mlp_pd.alpha,
            "Épocas de Entrenamiento": mlp_pd.n_iter_
        },
        "Regresor LGD (MLPRegressor)": {
            "Capas Ocultas": mlp_lgd.hidden_layer_sizes,
            "Activación Oculta": mlp_lgd.activation,
            "Optimizador": mlp_lgd.solver,
            "Épocas de Entrenamiento": mlp_lgd.n_iter_
        }
    })


# --- TAB 5: VIDEOS & SUSTENTACIÓN ---
with tab_videos:
    st.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #FCA5A5; text-transform: uppercase; margin-bottom: 4px;">
        MULTIMEDIA & SUSTENTACIÓN TÉCNICA
    </div>
    <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 20px;">
        Video promocional del producto y exposiciones individuales de cada integrante del equipo con evidencia técnica demostrativa.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;'>1. Video Promocional Oficial (Pitch Comercial · 2 a 3 min)</div>", unsafe_allow_html=True)
    col_vp1, col_vp2 = st.columns([3, 2])
    with col_vp1:
        st.video("https://youtu.be/lFPKU94AXQw")
    with col_vp2:
        st.markdown("""
        <div style="padding:16px; background:rgba(0,0,0,0.3); border-radius:10px; border:1px solid rgba(136,19,35,0.45); height:100%;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#EF4444; font-weight:700; text-transform:uppercase;">EVALUACIÓN Y ORIGINACIÓN</div>
            <div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin:6px 0;">Plataforma ¿Me prestas?</div>
            <p style="font-size:0.82rem; color:#94A3B8; line-height:1.6; margin-bottom:14px;">
                Presentación de la aplicación como solución tecnológica para analistas y comités de crédito: motor de clasificación binaria PD, calibración en escala estándar FICO 600 puntos, interpretabilidad marginal y cálculo de pérdida esperada bajo normas de Basilea II y III.
            </p>
            <a href="https://youtu.be/lFPKU94AXQw" target="_blank" style="display:inline-block; background:#DC2626; color:#FFF; padding:8px 16px; border-radius:6px; font-weight:700; font-size:0.78rem; text-decoration:none; font-family:'JetBrains Mono';">
                Abrir en YouTube ↗
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size:1rem; font-weight:700; color:#FFFFFF; margin-top:32px; margin-bottom:12px;'>2. Videos de Contribución Individual (Sustentación en Primera Persona)</div>", unsafe_allow_html=True)
    
    cv1, cv2 = st.columns(2)
    with cv1:
        st.markdown("""
        <div class="kpi-card" style="padding:16px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#00D2FF; font-weight:700;">STREAMLIT & WHAT-IF</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#94A3B8;">2:55 min</span>
            </div>
            <div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">David Agudelo Arboleda</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:10px;">
                Despliegue interactivo en Streamlit, implementación de Scorecard FICO/Basilea (S0=600, Odds 20:1, PDO=50) y motor What-If de sensibilidad.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=8MujIkYyee8")
        
        st.markdown("""
        <div class="kpi-card" style="padding:16px; margin-top:20px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#10B981; font-weight:700;">SEVERIDAD · LGD</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#94A3B8;">2:30 min</span>
            </div>
            <div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">Sara Osorio Piñerez</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:10px;">
                Modelado de Pérdida Dado el Incumplimiento (LGD), regresor MLP acotado en [0,1], contraste con modelos fraccionales y pérdida esperada.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=64bk3zrYsFU")

        st.markdown("""
        <div class="kpi-card" style="padding:16px; margin-top:20px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#F59E0B; font-weight:700;">AUDITORÍA & COHORTE MADURA</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#94A3B8;">2:50 min</span>
            </div>
            <div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">Santiago Álvarez Martínez (Baco)</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:10px;">
                Selección de cohorte Lending Club a 36 meses sin censura temporal, formulación y contraste empírico de las 4 hipótesis de riesgo.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=lRHa541LBnY")

    with cv2:
        st.markdown("""
        <div class="kpi-card" style="padding:16px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#EF4444; font-weight:700;">CALIBRACIÓN & REPORTE</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#94A3B8;">2:35 min</span>
            </div>
            <div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">Alejandro Agudelo Anaya</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:10px;">
                Regla de comparación justa frente a regresión logística, curvas de calibración, interpretabilidad por permutación y cacería de alucinaciones.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=m8Ez_CVvfpY")

        st.markdown("""
        <div class="kpi-card" style="padding:16px; margin-top:20px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-family:'JetBrains Mono'; font-size:0.75rem; color:#A855F7; font-weight:700;">PERCEPTRÓN MULTICAPA (PD)</span>
                <span style="font-family:'JetBrains Mono'; font-size:0.72rem; color:#94A3B8;">2:45 min</span>
            </div>
            <div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;">Daniel Felipe López Zapata</div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:10px;">
                Ajuste de hiperparámetros del clasificador MLP, funciones de activación ReLU/logistic, regularización L2 y estabilidad en 30 semillas.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.video("https://www.youtube.com/watch?v=9hN8B1hWywM")


# ------------------------------------------------------------------------------
# 8. PIE DE PÁGINA MINIMALISTA
# ------------------------------------------------------------------------------
st.markdown("<br><hr style='border: none; border-top: 1px solid var(--border-wine); margin: 30px 0 16px;'><br>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #94A3B8;">
    <div>UNIVERSIDAD NACIONAL DE COLOMBIA · REDES NEURONALES 2026-02</div>
    <div>¿ME PRESTAS? · SISTEMA DE INFERENCIA EN TIEMPO REAL</div>
</div>
""", unsafe_allow_html=True)
