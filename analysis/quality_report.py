"""
analysis/quality_report.py
Data Quality Report tab — score ring, issue cards, cleaning pipeline, PDF download.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from ui.components import sec_header, render_metrics, divider, report_card, code_step
from utils.metrics import (
    get_missing_stats, get_outlier_stats,
    get_high_correlations, compute_quality_score,
)


def show_quality_report(df: pd.DataFrame):
    sec_header("📝", "Data Quality Report", "Full audit summary with recommendations")

    # ── Compute all metrics ──────────────────────────────────
    missing_all   = df.isnull().sum()
    total_missing = int(missing_all.sum())
    missing_pct   = round(total_missing / df.size * 100, 2)
    n_dupes       = int(df.duplicated().sum())
    dupe_pct      = round(n_dupes / len(df) * 100, 2)

    out_df     = get_outlier_stats(df)
    out_cols   = out_df[out_df["Outlier Count"] > 0]["Column"].tolist()
    high_corr  = get_high_correlations(df)
    hc_count   = len(high_corr)

    score, grade, color = compute_quality_score(df)

    # ── Score ring ───────────────────────────────────────────
    circ = 2 * 3.14159 * 45
    dash = circ * score / 100

    st.markdown(f"""
    <div class="score-wrap">
        <div class="score-ring">
            <svg width="110" height="110" viewBox="0 0 110 110">
                <circle cx="55" cy="55" r="45" fill="none"
                    stroke="rgba(255,255,255,0.05)" stroke-width="10"/>
                <circle cx="55" cy="55" r="45" fill="none"
                    stroke="{color}" stroke-width="10"
                    stroke-dasharray="{dash:.1f} {circ:.1f}"
                    stroke-linecap="round"
                    style="filter:drop-shadow(0 0 6px {color}88)"/>
            </svg>
            <div class="score-num">
                <span class="n" style="color:{color};">{score}</span>
                <span class="d">/100</span>
            </div>
        </div>
        <div class="score-info">
            <div class="s-label">Data Quality Score</div>
            <div class="s-grade" style="background:{color}18;color:{color};border:1px solid {color}33;">
                {grade}
            </div>
            <div class="s-desc">
                Score is computed from missing values, duplicates, outliers and
                highly correlated features. Higher is better.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary metrics ──────────────────────────────────────
    render_metrics([
        ("🕳️","Missing %",    f"{missing_pct}%", f"{total_missing:,} cells",  "card-rose"    if missing_pct > 5 else "card-emerald"),
        ("🔁","Duplicates",   f"{n_dupes:,}",    f"{dupe_pct}% of rows",      "card-rose"    if n_dupes > 0     else "card-emerald"),
        ("📡","Outlier Cols", len(out_cols),      "columns flagged",           "card-amber"   if out_cols        else "card-emerald"),
        ("🔗","High Corr",    hc_count,           "pairs ≥ 0.8",              "card-amber"   if hc_count > 0    else "card-emerald"),
    ])

    divider()

    left, right = st.columns([1, 1])

    # ── Issue cards ──────────────────────────────────────────
    with left:
        sec_header("🩺", "Issue Analysis")

        # Missing values
        if total_missing == 0:
            report_card("#34d399", "✅ Missing Values — Clean",
                "No missing values detected. Dataset is 100% complete.")
        elif missing_pct < 5:
            top3 = missing_all[missing_all > 0].nlargest(3).index.tolist()
            report_card("#38bdf8", f"ℹ️ Missing Values — {missing_pct}%",
                f"{total_missing:,} null cells. Top columns: {', '.join(top3)}. "
                "Impute with mean/median for numeric, mode for categorical.")
        else:
            top3 = missing_all[missing_all > 0].nlargest(3).index.tolist()
            report_card("#fb7185", f"🚨 Missing Values — {missing_pct}% (High)",
                f"High nulls in: {', '.join(top3)}. Drop columns >50% missing; "
                "use KNN or iterative imputation for the rest.")

        # Duplicates
        if n_dupes == 0:
            report_card("#34d399", "✅ Duplicates — None Found",
                "All rows are unique. No deduplication needed.")
        elif dupe_pct < 2:
            report_card("#38bdf8", f"ℹ️ Duplicates — {n_dupes} rows ({dupe_pct}%)",
                "Low impact. Remove with: df.drop_duplicates()")
        else:
            report_card("#fbbf24", f"⚠️ Duplicates — {n_dupes} rows ({dupe_pct}%)",
                "Can bias ML model training. Remove before fitting.")

        # Outliers
        if not out_cols:
            report_card("#34d399", "✅ Outliers — None Detected",
                "IQR analysis found no significant outlier columns.")
        else:
            c = "#fbbf24" if len(out_cols) <= 3 else "#fb7185"
            report_card(c,
                f"{'⚠️' if len(out_cols)<=3 else '🚨'} Outliers — {len(out_cols)} columns",
                f"Affected: {', '.join(out_cols)}. "
                "Use IQR winsorization, log transform, or RobustScaler.")

        # Correlations
        if hc_count == 0:
            report_card("#34d399", "✅ Correlations — No Issues",
                "No feature pairs exceed the 0.8 correlation threshold.")
        else:
            c = "#fbbf24" if hc_count <= 3 else "#fb7185"
            report_card(c,
                f"{'⚠️' if hc_count<=3 else '🚨'} Correlations — {hc_count} pairs",
                "Multicollinearity risk. Consider PCA or dropping redundant features.")

    # ── Cleaning pipeline ────────────────────────────────────
    with right:
        sec_header("🛠️", "Cleaning Pipeline")

        steps = []
        if n_dupes > 0:
            steps.append(("Remove Duplicates",
                "df = df.drop_duplicates()\ndf = df.reset_index(drop=True)"))
        if total_missing > 0:
            steps.append(("Handle Missing Values",
                "# Numeric\ndf.fillna(df.median(numeric_only=True), inplace=True)\n"
                "# Categorical\ndf.fillna(df.mode().iloc[0], inplace=True)"))
        if out_cols:
            steps.append(("Cap Outliers (Winsorize)",
                "from scipy.stats import mstats\nfor col in outlier_cols:\n"
                "    df[col] = mstats.winsorize(\n        df[col], limits=[0.05, 0.05])"))
        if hc_count > 0:
            steps.append(("Reduce Multicollinearity",
                "from sklearn.decomposition import PCA\n# Or drop one from\n"
                "# each high-correlation pair manually"))
        steps.append(("Scale Features",
            "from sklearn.preprocessing import RobustScaler\nscaler = RobustScaler()\n"
            "df[num_cols] = scaler.fit_transform(df[num_cols])"))

        for idx, (title, code) in enumerate(steps, 1):
            code_step(idx, title, code)

    # ── PDF Download ─────────────────────────────────────────
    divider()
    sec_header("📥", "Download Report", "Export the full quality report as a PDF")

    st.markdown("""
    <div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.15);
                border-radius:14px;padding:20px 24px;margin-bottom:16px;">
        <div style="font-family:'Syne',sans-serif;font-size:15px;color:#e2e8f0;margin-bottom:6px;">
            📄 Full Data Quality Report
        </div>
        <div style="font-size:13px;color:#64748b;line-height:1.6;">
            Includes: Missing Values · Duplicates · Outliers ·
            Correlation matrix · Quality score · Cleaning recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        try:
            from generate_report import generate_pdf_report
            pdf_bytes = generate_pdf_report(df)
            fname = f"dq_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            st.download_button(
                label="⬇️  Download PDF Report",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"PDF generation failed: {e}")

    with col_info:
        st.markdown(f"""
        <div style="font-size:12px;color:#475569;line-height:1.8;padding-top:4px;">
            Format: <span style="color:#38bdf8;">PDF · A4</span>&nbsp;&nbsp;
            Dataset: <span style="color:#38bdf8;">{df.shape[0]:,} rows × {df.shape[1]} cols</span>&nbsp;&nbsp;
            Score: <span style="color:{color};">{score}/100</span>
        </div>""", unsafe_allow_html=True)