"""
analysis/correlations.py
Correlation Analysis tab — heatmap and high-correlation pairs.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from ui.components import sec_header, render_metrics, divider, info_box, success_box
from utils.metrics import get_high_correlations
from utils.plotting import C_ROSE, C_AMBER


def show_correlations(df: pd.DataFrame):
    sec_header("🔗", "Correlation Analysis", "Pearson correlation between numeric features")

    num_df = df.select_dtypes(include=np.number)

    if num_df.shape[1] < 2:
        st.warning("Need at least 2 numeric columns for correlation analysis.")
        return

    corr      = num_df.corr()
    high_corr = get_high_correlations(df)

    render_metrics([
        ("🔢", "Numeric Features",  num_df.shape[1],                        "analyzed",        "card-blue"),
        ("🔗", "High Corr Pairs",   len(high_corr),                         "threshold ≥ 0.8", "card-rose"),
        ("📐", "Total Pairs",       num_df.shape[1]*(num_df.shape[1]-1)//2, "combinations",    "card-violet"),
    ])

    divider()

    left, right = st.columns([1.8, 1])

    with left:
        sec_header("🗺️", "Correlation Heatmap", "Lower triangle · Pearson r")
        fig, ax = plt.subplots(
            figsize=(max(6, num_df.shape[1] * 0.95),
                     max(5, num_df.shape[1] * 0.9))
        )
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(217, 355, s=80, l=45, as_cmap=True)
        sns.heatmap(
            corr, mask=mask, ax=ax, cmap=cmap,
            vmin=-1, vmax=1, center=0,
            annot=True, fmt=".2f",
            annot_kws={"size": 9, "color": "#94a3b8"},
            linewidths=0.8, linecolor="#0b1120",
            cbar_kws={"shrink": .6, "pad": .02},
        )
        ax.set_title("Feature Correlation Matrix", fontsize=13, color="#e2e8f0", pad=16)
        ax.tick_params(labelsize=9)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with right:
        sec_header("⚡", "High Correlations", "Pairs with |r| ≥ 0.8")

        if high_corr:
            hc_df = pd.DataFrame(high_corr, columns=["Feature A", "Feature B", "r"])
            hc_df["Strength"] = hc_df["r"].abs().apply(
                lambda x: "🔴 ≥0.95" if x >= 0.95 else ("🟠 ≥0.90" if x >= 0.90 else "🟡 ≥0.80")
            )
            st.dataframe(hc_df, use_container_width=True, hide_index=True)
            st.markdown("<br>", unsafe_allow_html=True)
            info_box(
                "💡 Recommendation",
                "Highly correlated features can cause multicollinearity in linear models. "
                "Consider PCA, VIF analysis, or dropping one from each pair.",
            )
        else:
            success_box(
                "No High Correlations",
                "All feature pairs are below the 0.8 threshold.",
            )