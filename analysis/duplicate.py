"""
analysis/duplicates.py
Duplicate Detection tab.
"""

import streamlit as st
import pandas as pd

from ui.components import sec_header, render_metrics, divider, success_box, warning_box


def show_duplicates(df: pd.DataFrame):
    sec_header("🔁", "Duplicate Detection", "Identify repeated rows in the dataset")

    n_dupes  = int(df.duplicated().sum())
    dupe_pct = round(n_dupes / len(df) * 100, 2)
    unique   = len(df) - n_dupes

    render_metrics([
        ("📦", "Total Rows",     f"{len(df):,}", "in dataset",        "card-blue"),
        ("✅", "Unique Rows",    f"{unique:,}",  "distinct records",  "card-emerald"),
        ("🔁", "Duplicates",     f"{n_dupes:,}", "repeated rows",     "card-rose"),
        ("📊", "Duplicate Rate", f"{dupe_pct}%", "of all rows",       "card-amber"),
    ])

    divider()

    if n_dupes == 0:
        success_box("No Duplicates Found", "Every row in your dataset is unique.")
    else:
        warning_box(
            f"{n_dupes:,} duplicate rows detected ({dupe_pct}%)",
            "Fix: <code style='color:#38bdf8;'>df = df.drop_duplicates().reset_index(drop=True)</code>",
        )

        sec_header("🔍", "Duplicate Records", f"Showing all {n_dupes} flagged rows")
        dupes = df[df.duplicated(keep=False)]
        st.dataframe(
            dupes.style.apply(
                lambda x: ["background-color:rgba(251,113,133,0.08);color:#fb7185"] * len(x),
                axis=1,
            ),
            use_container_width=True,
            height=380,
        )