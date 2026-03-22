"""
analysis/missing_values.py
Missing Values Analysis tab.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from ui.components import sec_header, render_metrics, divider, success_box
from utils.metrics import get_missing_stats
from utils.plotting import C_BLUE, C_AMBER, C_ROSE


def show_missing_values(df: pd.DataFrame):
    sec_header("🕳️", "Missing Values Analysis", "Detect and visualize null data")

    mv_df      = get_missing_stats(df)
    total_mv   = int(df.isnull().sum().sum())
    cols_w_mv  = int((df.isnull().sum() > 0).sum())
    overall_pct= round(total_mv / df.size * 100, 2)

    render_metrics([
        ("📦", "Total Cells",      f"{df.size:,}", "in dataset",           "card-blue"),
        ("🕳️","Missing Cells",    f"{total_mv:,}","null values",           "card-rose"),
        ("📋", "Affected Columns", cols_w_mv,      f"of {df.shape[1]} cols","card-amber"),
        ("📉", "Overall Missing",  f"{overall_pct}%","of all cells",       "card-violet"),
    ])

    divider()

    left, right = st.columns([1, 1.7])

    with left:
        sec_header("📋", "Per-Column Table")
        st.dataframe(mv_df, use_container_width=True, hide_index=True, height=400)

    with right:
        sec_header("📊", "Missing Data Visualization")
        plot_df = mv_df[mv_df["Missing Count"] > 0]

        if plot_df.empty:
            success_box("Zero Missing Values!", "Your dataset is 100% complete.")
        else:
            fig, ax = plt.subplots(figsize=(8, max(3.5, len(plot_df) * 0.55)))
            colors = [
                C_ROSE  if v > 30 else
                C_AMBER if v > 10 else
                C_BLUE
                for v in plot_df["Missing %"]
            ]
            bars = ax.barh(
                plot_df["Column"], plot_df["Missing %"],
                color=colors, edgecolor="none", height=0.55,
            )
            ax.set_xlabel("Missing %", fontsize=10, color="#64748b")
            ax.set_title("Missing Values per Column", fontsize=13, color="#e2e8f0", pad=14)
            ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
            ax.set_xlim(0, max(plot_df["Missing %"]) * 1.18)
            ax.grid(axis="x", alpha=0.4)
            for bar, val in zip(bars, plot_df["Missing %"]):
                ax.text(
                    bar.get_width() + 0.4,
                    bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}%", va="center", fontsize=9, color="#64748b",
                )
            fig.tight_layout(pad=1.5)
            st.pyplot(fig)
            plt.close()