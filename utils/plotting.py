"""
utils/plotting.py
Shared matplotlib dark theme and color palette.
"""

import matplotlib.pyplot as plt

# ── Color Palette ─────────────────────────────────────────────
C_BLUE   = "#38bdf8"
C_VIOLET = "#818cf8"
C_GREEN  = "#34d399"
C_AMBER  = "#fbbf24"
C_ROSE   = "#fb7185"
C_TEAL   = "#2dd4bf"
PALETTE  = [C_BLUE, C_VIOLET, C_GREEN, C_AMBER, C_ROSE, C_TEAL, "#a78bfa", "#f97316"]


def set_plot_theme():
    """Apply the dark matplotlib theme globally."""
    plt.rcParams.update({
        "figure.facecolor":  "#0b1120",
        "axes.facecolor":    "#0b1120",
        "axes.edgecolor":    "#1e293b",
        "axes.labelcolor":   "#64748b",
        "axes.titlecolor":   "#e2e8f0",
        "axes.titlesize":    13,
        "axes.titlepad":     14,
        "xtick.color":       "#475569",
        "ytick.color":       "#475569",
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "grid.color":        "#1e293b",
        "grid.linestyle":    "--",
        "grid.alpha":        0.5,
        "text.color":        "#94a3b8",
        "font.family":       "monospace",
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.spines.left":  False,
        "axes.spines.bottom":True,
        "figure.dpi":        120,
    })