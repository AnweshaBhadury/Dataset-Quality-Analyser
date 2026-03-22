"""
analysis/outliers.py
Outlier Detection tab — IQR method with boxplots.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ui.components import sec_header, render_metrics, divider, badge
from utils.metrics import get_outlier_stats
from utils.plotting import C_ROSE, C_TEAL, C_GREEN


def show_outliers(df: pd.DataFrame):
    sec_header("📡", "Outlier Detection", "IQR method — 1.5× interquartile range")

    num_df = df.select_dtypes(include=np.number)

    if num_df.empty:
        st.warning("No numeric columns found in this dataset.")
        return

    out_df        = get_outlier_stats(df)
    cols_with_out = out_df[out_df["Outlier Count"] > 0]["Column"].tolist()

    render_metrics([
        ("🔢", "Numeric Columns",  len(num_df.columns),              "analyzed",      "card-blue"),
        ("📡", "Cols w/ Outliers", len(cols_with_out),               "need attention","card-rose"),
        ("✅", "Clean Columns",    len(num_df.columns) - len(cols_with_out), "no outliers","card-emerald"),
    ])

    divider()

    left, right = st.columns([1.6, 1])

    with left:
        sec_header("📦", "Boxplot Overview", "Each numeric column")
        ncols_p = min(len(num_df.columns), 4)
        nrows_p = (len(num_df.columns) + ncols_p - 1) // ncols_p
        fig, axes = plt.subplots(nrows_p, ncols_p,
                                 figsize=(ncols_p * 3.4, nrows_p * 3.2))
        axes = np.array(axes).flatten()

        for i, col in enumerate(num_df.columns):
            has_out  = col in cols_with_out
            bc = C_ROSE if has_out else C_TEAL
            axes[i].boxplot(
                num_df[col].dropna(),
                patch_artist=True, widths=0.5,
                boxprops=dict(facecolor=f"{bc}18", color=bc, linewidth=1.5),
                medianprops=dict(color=C_GREEN, linewidth=2.5),
                whiskerprops=dict(color="#334155", linewidth=1.2),
                capprops=dict(color="#334155", linewidth=1.5),
                flierprops=dict(marker="o", color=C_ROSE,
                               markerfacecolor=C_ROSE, markersize=3.5, alpha=0.6),
            )
            axes[i].set_title(col, fontsize=10, pad=8,
                              color=C_ROSE if has_out else "#94a3b8")
            axes[i].grid(axis="y", alpha=0.3)
            axes[i].tick_params(labelsize=8)

        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)

        fig.suptitle("Boxplots — Numeric Columns", fontsize=13, color="#e2e8f0", y=1.02)
        fig.tight_layout(pad=2)
        st.pyplot(fig)
        plt.close()

    with right:
        sec_header("📋", "Outlier Summary")
        display_df = out_df[["Column", "Outlier Count", "Status"]].copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        if cols_with_out:
            st.markdown("<br>", unsafe_allow_html=True)
            sec_header("🚨", "Flagged Columns")
            badges_html = "".join(
                badge(f"{c} · {out_df.loc[out_df['Column']==c,'Outlier Count'].values[0]}", "red")
                for c in cols_with_out
            )
            st.markdown(badges_html, unsafe_allow_html=True)