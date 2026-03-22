import streamlit as st
import pandas as pd
import numpy as np
import warnings
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Dataset Quality Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import load_css
from analysis.overview import show_overview
from analysis.missing_values import show_missing_values
from analysis.duplicate import show_duplicates
from analysis.outliers import show_outliers
from analysis.correlations import show_correlations
from analysis.quality_report import show_quality_report
from analysis.generate_report import show_generate_report

load_css()

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 20px;">
        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#e2e8f0;">🧬 DQ Analyzer</div>
        <div style="font-size:11px;color:#334155;font-family:'IBM Plex Mono',monospace;margin-top:3px;">v2.0 · Data Quality Suite</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.05);margin-bottom:20px;"></div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV Dataset", type=["csv"])

    df = None
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            num_c = df.select_dtypes(include=np.number).columns.tolist()
            cat_c = df.select_dtypes(exclude=np.number).columns.tolist()
            st.markdown(f"""
            <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.15);
                        border-radius:12px;padding:16px;margin-top:16px;">
                <div style="font-family:'Syne',sans-serif;font-size:14px;color:#e2e8f0;margin-bottom:12px;">
                    📄 {uploaded.name}</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px;text-align:center;">
                        <div style="font-size:20px;font-weight:700;color:#38bdf8;font-family:'Syne',sans-serif;">{df.shape[0]:,}</div>
                        <div style="font-size:10px;color:#475569;font-family:'IBM Plex Mono',monospace;">ROWS</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px;text-align:center;">
                        <div style="font-size:20px;font-weight:700;color:#818cf8;font-family:'Syne',sans-serif;">{df.shape[1]}</div>
                        <div style="font-size:10px;color:#475569;font-family:'IBM Plex Mono',monospace;">COLS</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px;text-align:center;">
                        <div style="font-size:20px;font-weight:700;color:#34d399;font-family:'Syne',sans-serif;">{len(num_c)}</div>
                        <div style="font-size:10px;color:#475569;font-family:'IBM Plex Mono',monospace;">NUMERIC</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.3);border-radius:8px;padding:10px;text-align:center;">
                        <div style="font-size:20px;font-weight:700;color:#fbbf24;font-family:'Syne',sans-serif;">{len(cat_c)}</div>
                        <div style="font-size:10px;color:#475569;font-family:'IBM Plex Mono',monospace;">CATEG.</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error reading file: {e}")

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.05);margin:20px 0;"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;color:#334155;font-family:monospace;text-align:center;">Upload a CSV to begin analysis</div>', unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">&#9658; Machine Learning &middot; Pre-processing Suite</div>
    <div class="hero-title">Dataset <span>Quality</span> Analyzer</div>
    <div class="hero-sub">Comprehensive data quality audit before you train. Detect missing values,
    duplicates, outliers, and correlation issues &mdash; all in one place.</div>
</div>
<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(56,189,248,0.25),rgba(139,92,246,0.2),transparent);margin-bottom:28px;"></div>
""", unsafe_allow_html=True)

if df is None:
    c = st.columns([1, 2, 1])[1]
    with c:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📂</div>
            <div class="es-title">No Dataset Loaded</div>
            <div class="es-sub">Upload a CSV file using the sidebar panel to begin your analysis.</div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# TABS
tabs = st.tabs([
    "📊  Overview",
    "🕳️  Missing Values",
    "🔁  Duplicates",
    "📡  Outliers",
    "🔗  Correlations",
    "📝  Quality Report",
    "📄  Export PDF",
])

with tabs[0]:
    show_overview(df)

with tabs[1]:
    show_missing_values(df)

with tabs[2]:
    show_duplicates(df)

with tabs[3]:
    show_outliers(df)

with tabs[4]:
    show_correlations(df)

with tabs[5]:
    show_quality_report(df)

with tabs[6]:
    show_generate_report(df)
