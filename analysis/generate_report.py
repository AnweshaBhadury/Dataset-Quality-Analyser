import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image as RLImage, KeepTogether, PageBreak,
)
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics import renderPDF
from datetime import datetime

BG        = colors.HexColor("#f8fafc")   # page background
CARD_BG   = colors.HexColor("#ffffff")   # card/table background
BORDER    = colors.HexColor("#e2e8f0")   # borders

C_BLUE    = colors.HexColor("#2563eb")   # primary accent
C_VIOLET  = colors.HexColor("#7c3aed")
C_GREEN   = colors.HexColor("#16a34a")   # success
C_AMBER   = colors.HexColor("#d97706")   # warning
C_ROSE    = colors.HexColor("#dc2626")   # error
C_TEAL    = colors.HexColor("#0d9488")   # secondary accent

C_SLATE   = colors.HexColor("#475569")   # secondary text
C_LIGHT   = colors.HexColor("#0f172a")   # primary text
C_MID     = colors.HexColor("#334155")   # table text
C_DIM     = colors.HexColor("#64748b")   # muted text

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# ── Paragraph styles ─────────────────────────────────────────
def _styles():
    return {
        "title": ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=26, textColor=C_LIGHT,
            leading=32, alignment=TA_LEFT),
        "subtitle": ParagraphStyle("subtitle",
            fontName="Helvetica", fontSize=11, textColor=C_SLATE,
            leading=16, alignment=TA_LEFT),
        "section": ParagraphStyle("section",
            fontName="Helvetica-Bold", fontSize=13, textColor=C_LIGHT,
            leading=18, spaceBefore=14, spaceAfter=6),
        "subsection": ParagraphStyle("subsection",
            fontName="Helvetica-Bold", fontSize=10, textColor=C_MID,
            leading=14, spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=9, textColor=C_MID,
            leading=14, spaceAfter=4),
        "mono": ParagraphStyle("mono",
            fontName="Courier", fontSize=8, textColor=C_BLUE,
            leading=12, backColor=colors.HexColor("#0a0f1c"),
            leftIndent=6, rightIndent=6, spaceBefore=4, spaceAfter=4),
        "badge_good": ParagraphStyle("badge_good",
            fontName="Helvetica-Bold", fontSize=8, textColor=C_GREEN,
            alignment=TA_CENTER),
        "badge_warn": ParagraphStyle("badge_warn",
            fontName="Helvetica-Bold", fontSize=8, textColor=C_AMBER,
            alignment=TA_CENTER),
        "badge_bad": ParagraphStyle("badge_bad",
            fontName="Helvetica-Bold", fontSize=8, textColor=C_ROSE,
            alignment=TA_CENTER),
        "label": ParagraphStyle("label",
            fontName="Helvetica", fontSize=7, textColor=C_SLATE,
            leading=10, alignment=TA_CENTER),
        "value": ParagraphStyle("value",
            fontName="Helvetica-Bold", fontSize=20, textColor=C_BLUE,
            leading=24, alignment=TA_CENTER),
        "small": ParagraphStyle("small",
            fontName="Helvetica", fontSize=7, textColor=C_SLATE,
            leading=10),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=7, textColor=C_DIM,
            alignment=TA_CENTER),
        "score_num": ParagraphStyle("score_num",
            fontName="Helvetica-Bold", fontSize=36, textColor=C_GREEN,
            leading=40, alignment=TA_CENTER),
        "score_label": ParagraphStyle("score_label",
            fontName="Helvetica-Bold", fontSize=11, textColor=C_LIGHT,
            leading=14, alignment=TA_LEFT),
        "score_sub": ParagraphStyle("score_sub",
            fontName="Helvetica", fontSize=9, textColor=C_SLATE,
            leading=13, alignment=TA_LEFT),
    }

# ── Helpers ──────────────────────────────────────────────────
def hr(color=BORDER, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=8, spaceBefore=4)

def spacer(h=6):
    return Spacer(1, h * mm)

def dark_table(data, col_widths, header_colors=None):
    """Returns a styled dark-theme Table."""
    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND",  (0, 0), (-1, 0),  colors.HexColor("#0d1929")),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  C_BLUE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  7.5),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8),
        ("TEXTCOLOR",   (0, 1), (-1, -1), C_MID),
        ("BACKGROUND",  (0, 1), (-1, -1), CARD_BG),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [CARD_BG, colors.HexColor("#111827")]),
        ("GRID",        (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
        ("ALIGN",       (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]
    tbl.setStyle(TableStyle(style))
    return tbl

def metric_card_table(cards):
    """
    cards = list of (label, value, sub, hex_color)
    Returns a single-row Table of metric cards.
    """
    S = _styles()
    n = len(cards)
    cell_w = (PAGE_W - 2 * MARGIN) / n

    cells = []
    for label, value, sub, hex_color in cards:
        vc = colors.HexColor(hex_color)
        cell = [
            Paragraph(f'<font color="{hex_color}"><b>{value}</b></font>',
                      ParagraphStyle("mv", fontName="Helvetica-Bold",
                                     fontSize=20, textColor=vc,
                                     leading=24, alignment=TA_CENTER)),
            Paragraph(label, S["label"]),
            Paragraph(sub,   S["small"] if sub else S["label"]),
        ]
        cells.append(cell)

    tbl = Table([cells], colWidths=[cell_w] * n)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), CARD_BG),
        ("BOX",          (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID",    (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tbl

def _mpl_theme():
    plt.rcParams.update({
        "figure.facecolor": "#0b1120", "axes.facecolor": "#0b1120",
        "axes.edgecolor": "#1e293b",   "axes.labelcolor": "#64748b",
        "axes.titlecolor": "#e2e8f0",  "axes.titlesize": 11,
        "xtick.color": "#475569",      "ytick.color": "#475569",
        "xtick.labelsize": 8,          "ytick.labelsize": 8,
        "grid.color": "#1e293b",       "grid.linestyle": "--",
        "grid.alpha": 0.5,             "text.color": "#94a3b8",
        "font.family": "monospace",
        "axes.spines.top": False,      "axes.spines.right": False,
        "axes.spines.left": False,     "axes.spines.bottom": True,
        "figure.dpi": 150,
    })

def fig_to_image(fig, width_mm):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    img = RLImage(buf, width=width_mm * mm)
    ar = fig.get_figheight() / fig.get_figwidth()
    img.drawHeight = img.drawWidth * ar
    plt.close(fig)
    return img

# ── Page canvas callback ─────────────────────────────────────
def _page_canvas(canvas, doc):
    canvas.saveState()
    # Dark background
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Top accent line
    canvas.setFillColor(C_BLUE)
    canvas.rect(0, PAGE_H - 2, PAGE_W, 2, fill=1, stroke=0)
    # Footer
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(C_DIM)
    canvas.drawCentredString(PAGE_W / 2, 10 * mm,
        f"Dataset Quality Analyzer  ·  Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}  ·  Page {doc.page}")
    canvas.restoreState()

# ── Section builder helpers ───────────────────────────────────
def _section_header(icon, title, subtitle=""):
    S = _styles()
    parts = [Paragraph(f"{icon}  {title}", S["section"])]
    if subtitle:
        parts.append(Paragraph(subtitle, S["small"]))
    parts.append(hr())
    return parts

# ═════════════════════════════════════════════════════════════
#  MAIN GENERATOR
# ═════════════════════════════════════════════════════════════
def generate_pdf_report(df: pd.DataFrame) -> bytes:
    _mpl_theme()
    S = _styles()
    buf = io.BytesIO()
    num_df = df.select_dtypes(include=np.number)

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 4*mm, bottomMargin=18*mm,
        title="Dataset Quality Report",
        author="DQ Analyzer v2.0",
    )

    story = []
    usable_w = PAGE_W - 2 * MARGIN

    # ── COVER / HEADER ────────────────────────────────────────
    now = datetime.now().strftime("%B %d, %Y  ·  %H:%M")
    story += [
        spacer(6),
        Paragraph("🧬  Dataset Quality Analyzer", S["subtitle"]),
        spacer(2),
        Paragraph("Data Quality Report", S["title"]),
        spacer(2),
        Paragraph(f"Generated: {now}", S["subtitle"]),
        spacer(4),
        hr(C_BLUE, 1),
        spacer(2),
    ]

    # ── SCORE ─────────────────────────────────────────────────
    missing_all   = df.isnull().sum()
    total_missing = int(missing_all.sum())
    missing_pct   = round(total_missing / df.size * 100, 2)
    n_dupes       = int(df.duplicated().sum())
    dupe_pct      = round(n_dupes / len(df) * 100, 2)
    completeness  = round((1 - df.isnull().sum().sum() / df.size) * 100, 1)

    out_cols = []
    for col in num_df.columns:
        q1, q3 = num_df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        if ((num_df[col] < q1-1.5*iqr)|(num_df[col] > q3+1.5*iqr)).sum() > 0:
            out_cols.append(col)

    hc_pairs = 0
    if num_df.shape[1] >= 2:
        corr = num_df.corr()
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if abs(corr.iloc[i,j]) >= 0.8:
                    hc_pairs += 1

    score = 100
    if missing_pct > 0: score -= min(30, missing_pct * 1.5)
    if dupe_pct > 0:    score -= min(20, dupe_pct * 2)
    if out_cols:        score -= min(20, len(out_cols) * 3)
    if hc_pairs:        score -= min(10, hc_pairs * 2)
    score = max(0, round(score))

    if score >= 80:   sc_hex, sg, sl = "#34d399", "Good",           "Your dataset is in good shape for ML."
    elif score >= 55: sc_hex, sg, sl = "#fbbf24", "Needs Attention","Some issues require cleaning before training."
    else:             sc_hex, sg, sl = "#fb7185", "Poor Quality",   "Significant data quality issues detected."

    score_color = colors.HexColor(sc_hex)

    score_tbl = Table(
        [[
            Paragraph(f'<font color="{sc_hex}"><b>{score}</b></font>',
                      ParagraphStyle("sn", fontName="Helvetica-Bold",
                                     fontSize=48, textColor=score_color,
                                     leading=52, alignment=TA_CENTER)),
            [
                Paragraph("Data Quality Score", S["score_label"]),
                Paragraph(
                    f'<font color="{sc_hex}"><b>{sg}</b></font>',
                    ParagraphStyle("sg", fontName="Helvetica-Bold", fontSize=10,
                                   textColor=score_color, leading=14)),
                spacer(1),
                Paragraph(sl, S["score_sub"]),
                spacer(1),
                Paragraph(
                    f"<b>Rows:</b> {df.shape[0]:,}  &nbsp;|&nbsp;  "
                    f"<b>Cols:</b> {df.shape[1]}  &nbsp;|&nbsp;  "
                    f"<b>Completeness:</b> {completeness}%",
                    S["small"]),
            ]
        ]],
        colWidths=[55*mm, usable_w - 55*mm],
    )
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), CARD_BG),
        ("BOX",          (0, 0), (-1, -1), 0.8, colors.HexColor(sc_hex)),
        ("INNERGRID",    (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 14),
        ("LEFTPADDING",  (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [score_tbl, spacer(4)]

    # ── TOP METRICS ───────────────────────────────────────────
    story.append(metric_card_table([
        ("Missing Cells",    f"{total_missing:,}",    f"{missing_pct}%",  "#fb7185" if missing_pct>5 else "#34d399"),
        ("Duplicate Rows",   f"{n_dupes:,}",          f"{dupe_pct}% of rows", "#fb7185" if n_dupes>0 else "#34d399"),
        ("Outlier Columns",  str(len(out_cols)),       "by IQR method",    "#fbbf24" if out_cols else "#34d399"),
        ("High Corr Pairs",  str(hc_pairs),           "threshold >= 0.8", "#fbbf24" if hc_pairs>0 else "#34d399"),
        ("Completeness",     f"{completeness}%",      "non-null cells",   "#34d399" if completeness>95 else "#fbbf24"),
    ]))
    story += [spacer(6), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 1  DATASET OVERVIEW
    # ════════════════════════════════════════════════════════
    story += _section_header("📊", "Dataset Overview",
                             "Shape, column types and descriptive statistics")

    # Schema table
    schema_data = [["Column", "Type", "Non-Null", "Null Count", "Null %"]]
    for col in df.columns:
        null_c = df[col].isnull().sum()
        null_p = f"{null_c/len(df)*100:.1f}%"
        schema_data.append([col, str(df[col].dtype),
                             str(df[col].count()), str(null_c), null_p])
    w = usable_w
    story.append(dark_table(schema_data,
        [w*0.32, w*0.16, w*0.16, w*0.18, w*0.18]))
    story.append(spacer(4))

    # Describe table
    if not num_df.empty:
        story.append(Paragraph("Descriptive Statistics (Numeric)", S["subsection"]))
        desc = df.describe().T.round(3).reset_index()
        desc.columns = [str(c) for c in desc.columns]
        desc_data = [desc.columns.tolist()] + desc.values.tolist()
        desc_data = [[str(v) for v in row] for row in desc_data]
        n_cols = len(desc_data[0])
        col_w = usable_w / n_cols
        story.append(dark_table(desc_data, [col_w] * n_cols))

    story += [spacer(4), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 2  MISSING VALUES
    # ════════════════════════════════════════════════════════
    story += _section_header("🕳️", "Missing Values Analysis",
                             "Null counts and percentages per column")

    mv_df = pd.DataFrame({
        "Column":        missing_all.index,
        "Missing Count": missing_all.values,
        "Missing %":     (missing_all / len(df) * 100).round(2).values,
        "Status":        ["Has Nulls" if v > 0 else "Complete" for v in missing_all.values],
    }).sort_values("Missing Count", ascending=False)

    mv_data = [["Column", "Missing Count", "Missing %", "Status"]]
    for _, row in mv_df.iterrows():
        mv_data.append([str(row["Column"]), str(row["Missing Count"]),
                        f"{row['Missing %']}%", row["Status"]])
    w = usable_w
    story.append(dark_table(mv_data, [w*0.4, w*0.2, w*0.2, w*0.2]))
    story.append(spacer(4))

    # Bar chart
    plot_df = mv_df[mv_df["Missing Count"] > 0]
    if not plot_df.empty:
        fig, ax = plt.subplots(figsize=(8, max(2.5, len(plot_df) * 0.45)))
        bar_colors = ["#fb7185" if v > 30 else "#fbbf24" if v > 10 else "#38bdf8"
                      for v in plot_df["Missing %"]]
        bars = ax.barh(plot_df["Column"], plot_df["Missing %"],
                       color=bar_colors, edgecolor="none", height=0.55)
        ax.set_xlabel("Missing %", fontsize=9, color="#64748b")
        ax.set_title("Missing Values per Column", fontsize=11, color="#e2e8f0", pad=10)
        ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
        ax.set_xlim(0, max(plot_df["Missing %"]) * 1.2)
        ax.grid(axis="x", alpha=0.4)
        for bar, val in zip(bars, plot_df["Missing %"]):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    f"{val:.1f}%", va="center", fontsize=8, color="#64748b")
        fig.tight_layout(pad=1.2)
        story.append(fig_to_image(fig, (usable_w / mm)))
    else:
        story.append(Paragraph("✅  No missing values — dataset is 100% complete.", S["body"]))

    story += [spacer(4), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 3  DUPLICATES
    # ════════════════════════════════════════════════════════
    story += _section_header("🔁", "Duplicate Detection",
                             "Repeated rows across the full dataset")

    unique_rows = len(df) - n_dupes
    dup_data = [
        ["Metric", "Value"],
        ["Total Rows",     f"{len(df):,}"],
        ["Unique Rows",    f"{unique_rows:,}"],
        ["Duplicate Rows", f"{n_dupes:,}"],
        ["Duplicate Rate", f"{dupe_pct}%"],
    ]
    story.append(dark_table(dup_data, [usable_w*0.5, usable_w*0.5]))
    story.append(spacer(3))

    if n_dupes == 0:
        story.append(Paragraph("✅  No duplicate rows found — all records are unique.", S["body"]))
    else:
        story.append(Paragraph(
            f"⚠️  {n_dupes:,} duplicate rows detected ({dupe_pct}%). "
            "Remove them with: df = df.drop_duplicates().reset_index(drop=True)", S["body"]))
        dupes_preview = df[df.duplicated(keep=False)].head(10)
        prev_data = [dupes_preview.columns.tolist()] + dupes_preview.values.tolist()
        prev_data = [[str(v) for v in row] for row in prev_data]
        n_c = len(prev_data[0])
        story.append(Paragraph("First 10 duplicate rows (preview):", S["subsection"]))
        story.append(dark_table(prev_data, [usable_w / n_c] * n_c))

    story += [spacer(4), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 4  OUTLIERS
    # ════════════════════════════════════════════════════════
    story += _section_header("📡", "Outlier Detection",
                             "IQR method — 1.5x interquartile range")

    if num_df.empty:
        story.append(Paragraph("No numeric columns found.", S["body"]))
    else:
        outlier_data = {}
        for col in num_df.columns:
            q1, q3 = num_df[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
            n_out = int(((num_df[col] < lo) | (num_df[col] > hi)).sum())
            outlier_data[col] = {"Q1": round(q1, 3), "Q3": round(q3, 3),
                                  "IQR": round(iqr, 3), "Lower": round(lo, 3),
                                  "Upper": round(hi, 3), "Outliers": n_out}

        out_tbl_data = [["Column", "Q1", "Q3", "IQR", "Lower", "Upper", "Outliers", "Status"]]
        for col, d in outlier_data.items():
            status = "⚠ Yes" if d["Outliers"] > 0 else "✓ Clean"
            out_tbl_data.append([col, str(d["Q1"]), str(d["Q3"]), str(d["IQR"]),
                                  str(d["Lower"]), str(d["Upper"]),
                                  str(d["Outliers"]), status])
        w = usable_w
        story.append(dark_table(out_tbl_data,
            [w*0.20, w*0.09, w*0.09, w*0.09, w*0.12, w*0.12, w*0.13, w*0.16]))
        story.append(spacer(4))

        # Boxplots
        story.append(Paragraph("Boxplot Overview", S["subsection"]))
        ncols_p = min(len(num_df.columns), 4)
        nrows_p = (len(num_df.columns) + ncols_p - 1) // ncols_p
        fig, axes = plt.subplots(nrows_p, ncols_p,
                                 figsize=(ncols_p * 3.2, nrows_p * 3.0))
        axes = np.array(axes).flatten()
        for i, col in enumerate(num_df.columns):
            has_out = col in out_cols
            bc = "#fb7185" if has_out else "#2dd4bf"
            axes[i].boxplot(num_df[col].dropna(), patch_artist=True, widths=0.5,
                boxprops=dict(facecolor=f"{bc}22", color=bc, linewidth=1.5),
                medianprops=dict(color="#34d399", linewidth=2),
                whiskerprops=dict(color="#334155", linewidth=1.2),
                capprops=dict(color="#334155", linewidth=1.5),
                flierprops=dict(marker="o", color="#fb7185",
                               markerfacecolor="#fb7185", markersize=3, alpha=0.6))
            axes[i].set_title(col, fontsize=9, pad=6,
                              color="#fb7185" if has_out else "#94a3b8")
            axes[i].grid(axis="y", alpha=0.3)
            axes[i].tick_params(labelsize=7)
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)
        fig.suptitle("Boxplots — Numeric Columns", fontsize=11, color="#e2e8f0", y=1.01)
        fig.tight_layout(pad=1.8)
        story.append(fig_to_image(fig, usable_w / mm))

    story += [spacer(4), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 5  CORRELATIONS
    # ════════════════════════════════════════════════════════
    story += _section_header("🔗", "Correlation Analysis",
                             "Pearson correlation between numeric features")

    if num_df.shape[1] < 2:
        story.append(Paragraph("Need at least 2 numeric columns for correlation analysis.", S["body"]))
    else:
        corr = num_df.corr()
        high_corr_list = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                v = corr.iloc[i, j]
                if abs(v) >= 0.8:
                    high_corr_list.append((corr.columns[i], corr.columns[j], round(v, 3)))

        # Heatmap
        fig, ax = plt.subplots(figsize=(max(5, num_df.shape[1]*0.9),
                                        max(4, num_df.shape[1]*0.85)))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(217, 355, s=80, l=45, as_cmap=True)
        sns.heatmap(corr, mask=mask, ax=ax, cmap=cmap, vmin=-1, vmax=1, center=0,
                    annot=True, fmt=".2f", annot_kws={"size": 8, "color": "#94a3b8"},
                    linewidths=0.8, linecolor="#0b1120",
                    cbar_kws={"shrink": .6, "pad": .02})
        ax.set_title("Feature Correlation Matrix (Pearson r)", fontsize=11,
                     color="#e2e8f0", pad=12)
        ax.tick_params(labelsize=8)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        fig.tight_layout()
        story.append(fig_to_image(fig, usable_w / mm))
        story.append(spacer(4))

        # High correlation table
        if high_corr_list:
            story.append(Paragraph(f"High Correlation Pairs  (|r| >= 0.8)", S["subsection"]))
            hc_data = [["Feature A", "Feature B", "r", "Strength"]]
            for fa, fb, r in high_corr_list:
                strength = "Very High (>=0.95)" if abs(r)>=0.95 else \
                           "High (>=0.90)" if abs(r)>=0.90 else "Moderate (>=0.80)"
                hc_data.append([fa, fb, str(r), strength])
            story.append(dark_table(hc_data, [usable_w*0.3, usable_w*0.3,
                                               usable_w*0.15, usable_w*0.25]))
            story.append(spacer(2))
            story.append(Paragraph(
                "Recommendation: Highly correlated features can cause multicollinearity. "
                "Consider PCA, VIF analysis, or dropping one feature from each pair.",
                S["body"]))
        else:
            story.append(Paragraph(
                "✅  No feature pairs exceed the 0.8 correlation threshold.", S["body"]))

    story += [spacer(4), PageBreak()]

    # ════════════════════════════════════════════════════════
    # 6  QUALITY REPORT & CLEANING PIPELINE
    # ════════════════════════════════════════════════════════
    story += _section_header("📝", "Quality Report & Recommendations",
                             "Issue summary and suggested cleaning pipeline")

    # Issue analysis rows
    issues = []
    # Missing
    if total_missing == 0:
        issues.append(("✅", "Missing Values", "Clean", "No missing values detected.", "#34d399"))
    elif missing_pct < 5:
        top3 = missing_all[missing_all>0].nlargest(3).index.tolist()
        issues.append(("ℹ", "Missing Values", f"{missing_pct}%",
                       f"Low ({total_missing:,} cells). Top: {', '.join(top3)}. "
                       "Impute with mean/median or mode.", "#38bdf8"))
    else:
        top3 = missing_all[missing_all>0].nlargest(3).index.tolist()
        issues.append(("🚨", "Missing Values", f"{missing_pct}% (High)",
                       f"Significant nulls in {', '.join(top3)}. "
                       "Drop cols >50% missing; use KNN imputation for rest.", "#fb7185"))

    # Duplicates
    if n_dupes == 0:
        issues.append(("✅", "Duplicates", "None", "All rows unique.", "#34d399"))
    elif dupe_pct < 2:
        issues.append(("ℹ", "Duplicates", f"{n_dupes:,} rows",
                       "Low impact. Remove with df.drop_duplicates().", "#38bdf8"))
    else:
        issues.append(("⚠", "Duplicates", f"{n_dupes:,} rows ({dupe_pct}%)",
                       "Can bias ML training. Remove before fitting.", "#fbbf24"))

    # Outliers
    if not out_cols:
        issues.append(("✅", "Outliers", "None", "IQR analysis found no outlier columns.", "#34d399"))
    elif len(out_cols) <= 3:
        issues.append(("⚠", "Outliers", f"{len(out_cols)} columns",
                       f"Affected: {', '.join(out_cols)}. Use winsorization or RobustScaler.", "#fbbf24"))
    else:
        issues.append(("🚨", "Outliers", f"{len(out_cols)} columns",
                       f"Many cols flagged: {', '.join(out_cols[:5])}... "
                       "Consider log transform or IQR capping.", "#fb7185"))

    # Correlations
    if hc_pairs == 0:
        issues.append(("✅", "Correlations", "No issues", "All pairs below 0.8 threshold.", "#34d399"))
    elif hc_pairs <= 3:
        issues.append(("⚠", "Correlations", f"{hc_pairs} pairs",
                       "Moderate multicollinearity risk. Review with VIF analysis.", "#fbbf24"))
    else:
        issues.append(("🚨", "Correlations", f"{hc_pairs} pairs",
                       "High multicollinearity. Apply PCA or drop redundant features.", "#fb7185"))

    issue_data = [["", "Issue", "Status", "Recommendation"]]
    for icon, issue, status, rec, color in issues:
        issue_data.append([icon, issue, status, rec])

    tbl = Table(issue_data, colWidths=[usable_w*0.04, usable_w*0.15,
                                        usable_w*0.18, usable_w*0.63])
    style = [
        ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#0d1929")),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  C_BLUE),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 8),
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",    (0, 1), (-1, -1), C_MID),
        ("BACKGROUND",   (0, 1), (-1, -1), CARD_BG),
        ("ROWBACKGROUNDS",(0, 1),(-1, -1), [CARD_BG, colors.HexColor("#111827")]),
        ("GRID",         (0, 0), (-1, -1), 0.3, BORDER),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
    ]
    for i, (_, _, _, _, color) in enumerate(issues, 1):
        tbl.setStyle(TableStyle([
            ("TEXTCOLOR", (1, i), (2, i), colors.HexColor(color)),
            ("FONTNAME",  (1, i), (2, i), "Helvetica-Bold"),
        ]))
    tbl.setStyle(TableStyle(style))
    story.append(tbl)
    story.append(spacer(6))

    # ── Cleaning pipeline ──────────────────────────────────
    story.append(Paragraph("Suggested Cleaning Pipeline", S["subsection"]))

    steps = []
    if n_dupes > 0:
        steps.append(("1. Remove Duplicates",
                      "df = df.drop_duplicates()\ndf = df.reset_index(drop=True)"))
    if total_missing > 0:
        steps.append(("2. Handle Missing Values",
                      "df.fillna(df.median(numeric_only=True), inplace=True)  # numeric\n"
                      "df.fillna(df.mode().iloc[0], inplace=True)             # categorical"))
    if out_cols:
        steps.append(("3. Cap Outliers (Winsorize)",
                      "from scipy.stats import mstats\nfor col in outlier_cols:\n"
                      "    df[col] = mstats.winsorize(df[col], limits=[0.05, 0.05])"))
    if hc_pairs > 0:
        steps.append(("4. Reduce Multicollinearity",
                      "from sklearn.decomposition import PCA\n"
                      "# Or manually drop one feature from each high-corr pair"))
    steps.append((f"{len(steps)+1}. Scale Features",
                  "from sklearn.preprocessing import RobustScaler\n"
                  "scaler = RobustScaler()\n"
                  "df[num_cols] = scaler.fit_transform(df[num_cols])"))

    for step_title, code in steps:
        story.append(KeepTogether([
            Paragraph(step_title, S["subsection"]),
            Paragraph(code, S["mono"]),
            spacer(2),
        ]))

    # ── Build ──────────────────────────────────────────────
    doc.build(story, onFirstPage=_page_canvas, onLaterPages=_page_canvas)
    buf.seek(0)
    return buf.read()


# ═════════════════════════════════════════════════════════════
#  STREAMLIT TAB RENDERER
# ═════════════════════════════════════════════════════════════
def show_generate_report(df: pd.DataFrame):
    from ui.components import sec_header, divider

    sec_header("📄", "Generate PDF Report",
               "Download a full data quality audit as a styled PDF")
    divider()

    st.markdown("""
    <div style="background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.15);
                border-radius:14px;padding:20px 24px;margin-bottom:24px;">
        <div style="font-family:'Syne',sans-serif;font-size:15px;color:#e2e8f0;margin-bottom:8px;">
            📋 What's included in the report?</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;">
            ✦ &nbsp;<b style="color:#94a3b8;">Data Quality Score</b> — overall audit score out of 100<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Dataset Overview</b> — schema, types, descriptive stats<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Missing Values</b> — per-column counts, percentages, bar chart<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Duplicates</b> — count, rate, preview of flagged rows<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Outliers</b> — IQR table + boxplot visualizations<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Correlations</b> — heatmap + high-correlation pairs table<br>
            ✦ &nbsp;<b style="color:#94a3b8;">Cleaning Pipeline</b> — ready-to-use Python code snippets
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("⬇️  Generate & Download PDF Report",
                     use_container_width=True, type="primary"):
            with st.spinner("Building your PDF report..."):
                pdf_bytes = generate_pdf_report(df)

            fname = f"dq_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            st.download_button(
                label="📄  Click here to download the PDF",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True,
            )
            st.success("Report ready! Click the button above to save it.")
