"""
analysis/overview.py
Dataset Overview tab — shape, schema, stats, preview.
"""

import streamlit as st
import pandas as pd
import numpy as np

from ui.components import sec_header, render_metrics, divider


def show_overview(df: pd.DataFrame):
    sec_header("📊", "Dataset Overview", "Shape, types, statistics and preview")

    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(exclude=np.number).columns
    completeness = round((1 - df.isnull().sum().sum() / df.size) * 100, 1)

    render_metrics([
        ("🗂️", "Total Rows",    f"{df.shape[0]:,}", f"{df.shape[0]:,} records",         "card-blue"),
        ("📐", "Columns",        df.shape[1],         "features total",                   "card-violet"),
        ("🔢", "Numeric Cols",  len(num_cols),        "numeric features",                 "card-emerald"),
        ("🏷️","Categorical",   len(cat_cols),        "object columns",                   "card-amber"),
        ("✅", "Completeness",  f"{completeness}%",  "non-null cells",                   "card-teal"),
    ])

    divider()

    left, right = st.columns([1.1, 1])

    with left:
        sec_header("🏷️", "Column Schema", "Names, types and null counts")
        schema_df = pd.DataFrame({
            "Column":     df.columns,
            "Type":       df.dtypes.astype(str).values,
            "Non-Null":   df.count().values,
            "Null Count": df.isnull().sum().values,
            "Null %":     (df.isnull().mean() * 100).round(1).astype(str).add("%").values,
        })
        st.dataframe(schema_df, use_container_width=True, hide_index=True, height=320)

    with right:
        sec_header("📈", "Descriptive Statistics", "Numeric columns summary")
        st.dataframe(df.describe().T.round(3), use_container_width=True, height=320)

    divider()
    sec_header("👀", "Data Preview", "First 10 rows of the dataset")
    st.dataframe(df.head(10), use_container_width=True)