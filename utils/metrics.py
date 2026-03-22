"""
utils/metrics.py
Shared computation helpers used across analysis modules.
"""

import pandas as pd
import numpy as np


def get_missing_stats(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    pct     = (missing / len(df) * 100).round(2)
    return pd.DataFrame({
        "Column":        missing.index,
        "Missing Count": missing.values,
        "Missing %":     pct.values,
        "Status":        ["⚠️ Has Nulls" if v > 0 else "✅ Complete" for v in missing.values],
    }).sort_values("Missing Count", ascending=False).reset_index(drop=True)


def get_outlier_stats(df: pd.DataFrame) -> pd.DataFrame:
    num_df = df.select_dtypes(include=np.number)
    rows = []
    for col in num_df.columns:
        q1, q3 = num_df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((num_df[col] < lo) | (num_df[col] > hi)).sum())
        rows.append({
            "Column":      col,
            "Q1":          round(q1, 3),
            "Q3":          round(q3, 3),
            "IQR":         round(iqr, 3),
            "Lower Bound": round(lo, 3),
            "Upper Bound": round(hi, 3),
            "Outlier Count": n_out,
            "Status":      "⚠️ Outliers" if n_out > 0 else "✅ Clean",
        })
    return pd.DataFrame(rows)


def get_high_correlations(df: pd.DataFrame, threshold: float = 0.8) -> list[tuple]:
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return []
    corr = num_df.corr()
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            v = corr.iloc[i, j]
            if abs(v) >= threshold:
                pairs.append((corr.columns[i], corr.columns[j], round(v, 3)))
    return pairs


def compute_quality_score(df: pd.DataFrame) -> tuple[int, str, str]:
    """Returns (score, grade_label, grade_color)."""
    missing_pct = df.isnull().sum().sum() / df.size * 100
    dupe_pct    = df.duplicated().sum() / len(df) * 100
    out_cols    = get_outlier_stats(df)
    out_count   = len(out_cols[out_cols["Outlier Count"] > 0])
    hc_count    = len(get_high_correlations(df))

    score = 100
    if missing_pct > 0: score -= min(30, missing_pct * 1.5)
    if dupe_pct > 0:    score -= min(20, dupe_pct * 2)
    if out_count > 0:   score -= min(20, out_count * 3)
    if hc_count > 0:    score -= min(10, hc_count * 2)
    score = max(0, round(score))

    if score >= 80:   return score, "Good",           "#34d399"
    elif score >= 55: return score, "Needs Attention", "#fbbf24"
    else:             return score, "Poor Quality",    "#fb7185"