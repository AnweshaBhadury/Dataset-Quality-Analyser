"""
ui/styles.py
Global CSS theme for the Dataset Quality Analyzer.

Usage:
    from ui.styles import load_css
    load_css()
"""

import streamlit as st


def load_css():
    st.markdown("""
    <style>

    /* ── Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@300;400;500;600&display=swap');

    /* ── Reset & Base ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html, body, [class*="css"] { font-family: 'Manrope', sans-serif; color: #e2e8f0; }

    /* ── App Background ── */
    .stApp {
        background: #080c14;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(139,92,246,0.06) 0%, transparent 55%);
        min-height: 100vh;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(10,15,28,0.97) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label span {
        color: #94a3b8 !important;
        font-size: 13px;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
        font-family: 'Syne', sans-serif !important;
    }
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px dashed rgba(56,189,248,0.3) !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }

    /* ── Tabs ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 28px;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #64748b;
        font-family: 'Manrope', sans-serif;
        font-size: 13px;
        font-weight: 500;
        padding: 8px 18px;
        border: none;
        transition: all 0.2s ease;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(139,92,246,0.15)) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56,189,248,0.25) !important;
        font-weight: 600;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"],
    [data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }

    /* ── Metric Cards ── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
        gap: 16px;
        margin: 20px 0 32px 0;
    }
    .metric-card {
        position: relative;
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 22px 20px;
        overflow: hidden;
        transition: transform 0.2s, border-color 0.2s;
        animation: fadeSlideUp 0.4s ease both;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: var(--ag, linear-gradient(90deg, #38bdf8, #818cf8));
        border-radius: 16px 16px 0 0;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 100px; height: 100px;
        background: var(--glow, rgba(56,189,248,0.06));
        border-radius: 50%;
        filter: blur(20px);
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.2);
    }
    .m-icon  { font-size: 20px; margin-bottom: 10px; display: block; }
    .m-label {
        font-size: 11px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #475569;
        font-family: 'IBM Plex Mono', monospace;
        margin-bottom: 6px;
    }
    .m-value {
        font-size: 30px;
        font-weight: 700;
        font-family: 'Syne', sans-serif;
        color: var(--vc, #38bdf8);
        line-height: 1;
    }
    .m-sub {
        font-size: 11px;
        color: #475569;
        margin-top: 6px;
        font-family: 'IBM Plex Mono', monospace;
    }

    /* Metric card color variants */
    .card-blue    { --ag: linear-gradient(90deg,#38bdf8,#60a5fa); --vc: #38bdf8; --glow: rgba(56,189,248,0.08); }
    .card-violet  { --ag: linear-gradient(90deg,#818cf8,#a78bfa); --vc: #818cf8; --glow: rgba(129,140,248,0.08); }
    .card-emerald { --ag: linear-gradient(90deg,#34d399,#10b981); --vc: #34d399; --glow: rgba(52,211,153,0.08); }
    .card-amber   { --ag: linear-gradient(90deg,#fbbf24,#f59e0b); --vc: #fbbf24; --glow: rgba(251,191,36,0.08); }
    .card-rose    { --ag: linear-gradient(90deg,#fb7185,#f43f5e); --vc: #fb7185; --glow: rgba(251,113,133,0.08); }
    .card-teal    { --ag: linear-gradient(90deg,#2dd4bf,#14b8a6); --vc: #2dd4bf; --glow: rgba(45,212,191,0.08); }

    /* ── Section Headers ── */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0 0 20px 0;
    }
    .sh-icon {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, rgba(56,189,248,0.15), rgba(139,92,246,0.15));
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    .sh-title {
        font-family: 'Syne', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #e2e8f0;
    }
    .sh-sub { font-size: 12px; color: #475569; margin-top: 1px; }

    /* ── Data Tables ── */
    .dataframe {
        background: transparent !important;
        font-size: 12.5px !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    .dataframe thead tr th {
        background: rgba(56,189,248,0.08) !important;
        color: #38bdf8 !important;
        font-size: 11px !important;
        letter-spacing: 0.08em;
        padding: 10px 14px !important;
        border-bottom: 1px solid rgba(56,189,248,0.15) !important;
    }
    .dataframe tbody tr td {
        background: rgba(15,23,42,0.4) !important;
        color: #94a3b8 !important;
        padding: 9px 14px !important;
        border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    }
    .dataframe tbody tr:hover td {
        background: rgba(56,189,248,0.06) !important;
        color: #e2e8f0 !important;
    }

    /* ── Report Cards ── */
    .report-card {
        display: flex;
        gap: 16px;
        align-items: flex-start;
        background: rgba(15,23,42,0.7);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }
    .report-card:hover { border-color: rgba(255,255,255,0.12); }
    .rc-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        margin-top: 5px;
        flex-shrink: 0;
    }
    .rc-body h4 {
        font-family: 'Syne', sans-serif;
        font-size: 15px;
        color: #e2e8f0;
        margin-bottom: 4px;
    }
    .rc-body p { font-size: 13px; color: #64748b; line-height: 1.65; }

    /* ── Quality Score Ring ── */
    .score-wrap {
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 32px 40px;
        display: flex;
        align-items: center;
        gap: 40px;
        margin-bottom: 28px;
    }
    .score-ring { position: relative; width: 110px; height: 110px; flex-shrink: 0; }
    .score-ring svg { transform: rotate(-90deg); }
    .score-ring .score-num {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'Syne', sans-serif;
    }
    .score-ring .score-num .n { font-size: 28px; font-weight: 800; }
    .score-ring .score-num .d {
        font-size: 10px;
        color: #475569;
        font-family: 'IBM Plex Mono', monospace;
    }
    .score-info .s-label {
        font-family: 'Syne', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 4px;
    }
    .score-info .s-grade {
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-family: 'IBM Plex Mono', monospace;
        margin-bottom: 10px;
    }
    .score-info .s-desc {
        font-size: 13px;
        color: #475569;
        max-width: 480px;
        line-height: 1.6;
    }

    /* ── Hero ── */
    .hero { padding: 4px 0 28px; }
    .hero-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #38bdf8;
        margin-bottom: 10px;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 38px;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1.15;
        margin-bottom: 10px;
    }
    .hero-title span {
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub { font-size: 15px; color: #475569; line-height: 1.7; max-width: 620px; }

    /* ── Empty State ── */
    .empty-state {
        text-align: center;
        padding: 80px 40px;
        background: rgba(15,23,42,0.5);
        border: 1px dashed rgba(255,255,255,0.08);
        border-radius: 20px;
        margin-top: 20px;
    }
    .empty-state .es-icon  { font-size: 52px; margin-bottom: 16px; }
    .empty-state .es-title {
        font-family: 'Syne', sans-serif;
        font-size: 20px;
        color: #e2e8f0;
        margin-bottom: 8px;
    }
    .empty-state .es-sub { font-size: 14px; color: #475569; }

    /* ── Fancy Divider ── */
    .fancy-divider {
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(56,189,248,0.2),
            rgba(139,92,246,0.2),
            transparent
        );
        margin: 28px 0;
    }

    /* ── Code Block ── */
    .code-block {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.06);
        border-left: 3px solid #38bdf8;
        border-radius: 10px;
        padding: 14px 18px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: #94a3b8;
        overflow-x: auto;
        margin-top: 8px;
        white-space: pre;
    }

    /* ── Badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.03em;
    }
    .badge-blue  { background: rgba(56,189,248,0.12);  color: #38bdf8; border: 1px solid rgba(56,189,248,0.2); }
    .badge-red   { background: rgba(251,113,133,0.12); color: #fb7185; border: 1px solid rgba(251,113,133,0.2); }
    .badge-green { background: rgba(52,211,153,0.12);  color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
    .badge-amber { background: rgba(251,191,36,0.12);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }

    /* ── Animations ── */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Streamlit Overrides ── */
    [data-testid="stMarkdownContainer"] h4 {
        font-family: 'Syne', sans-serif !important;
        color: #cbd5e1 !important;
        font-size: 15px !important;
        margin-bottom: 12px !important;
    }

    </style>
    """, unsafe_allow_html=True)