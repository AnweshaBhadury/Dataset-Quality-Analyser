"""
ui/components.py
Reusable HTML component helpers used across all analysis modules.
"""

import streamlit as st


def sec_header(icon: str, title: str, subtitle: str = ""):
    sub = f'<div class="sh-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="sec-header">
        <div class="sh-icon">{icon}</div>
        <div><div class="sh-title">{title}</div>{sub}</div>
    </div>""", unsafe_allow_html=True)


def render_metrics(cards: list):
    """
    cards: list of (icon, label, value, sub, css_class)
    """
    html = '<div class="metric-grid">'
    for i, (icon, label, value, sub, cls) in enumerate(cards):
        html += f"""
        <div class="metric-card {cls}" style="animation-delay:{i * 0.07}s;">
            <span class="m-icon">{icon}</span>
            <div class="m-label">{label}</div>
            <div class="m-value">{value}</div>
            <div class="m-sub">{sub}</div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


def report_card(dot_color: str, title: str, body: str):
    st.markdown(f"""
    <div class="report-card">
        <div class="rc-dot" style="background:{dot_color};box-shadow:0 0 8px {dot_color}55;"></div>
        <div class="rc-body"><h4>{title}</h4><p>{body}</p></div>
    </div>""", unsafe_allow_html=True)


def empty_state(icon: str, title: str, subtitle: str):
    st.markdown(f"""
    <div class="empty-state">
        <div class="es-icon">{icon}</div>
        <div class="es-title">{title}</div>
        <div class="es-sub">{subtitle}</div>
    </div>""", unsafe_allow_html=True)


def success_box(title: str, body: str):
    st.markdown(f"""
    <div style="background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.2);
                border-radius:16px;padding:32px;text-align:center;">
        <div style="font-size:32px;margin-bottom:10px;">🎉</div>
        <div style="font-family:'Syne',sans-serif;font-size:18px;color:#34d399;margin-bottom:6px;">{title}</div>
        <div style="font-size:13px;color:#475569;">{body}</div>
    </div>""", unsafe_allow_html=True)


def warning_box(title: str, body: str):
    st.markdown(f"""
    <div style="background:rgba(251,113,133,0.06);border:1px solid rgba(251,113,133,0.2);
                border-radius:14px;padding:18px 22px;margin-bottom:20px;
                display:flex;align-items:center;gap:14px;">
        <div style="font-size:24px;">⚠️</div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:15px;color:#fb7185;">{title}</div>
            <div style="font-size:13px;color:#475569;margin-top:3px;">{body}</div>
        </div>
    </div>""", unsafe_allow_html=True)


def info_box(title: str, body: str):
    st.markdown(f"""
    <div style="background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.2);
                border-radius:12px;padding:14px 16px;">
        <div style="font-size:12px;color:#fbbf24;font-weight:600;margin-bottom:6px;">{title}</div>
        <div style="font-size:12px;color:#64748b;line-height:1.6;">{body}</div>
    </div>""", unsafe_allow_html=True)


def badge(text: str, color: str = "blue") -> str:
    return f'<span class="badge badge-{color}" style="margin:3px 3px 3px 0;display:inline-block;">{text}</span>'


def code_step(idx: int, title: str, code: str):
    st.markdown(f"""
    <div style="background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.07);
                border-radius:12px;padding:16px 18px;margin-bottom:12px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
            <div style="width:22px;height:22px;border-radius:6px;
                        background:linear-gradient(135deg,rgba(56,189,248,0.2),rgba(129,140,248,0.2));
                        border:1px solid rgba(56,189,248,0.2);
                        display:flex;align-items:center;justify-content:center;
                        font-size:11px;font-weight:700;color:#38bdf8;
                        font-family:'IBM Plex Mono',monospace;">{idx}</div>
            <div style="font-family:'Syne',sans-serif;font-size:14px;
                        color:#e2e8f0;font-weight:600;">{title}</div>
        </div>
        <div class="code-block">{code}</div>
    </div>""", unsafe_allow_html=True)