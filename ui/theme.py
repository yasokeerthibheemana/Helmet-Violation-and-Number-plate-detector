"""
ui/theme.py — Clean pastel theme for Helmet Detection app
Usage: from ui.theme import inject_theme, section_card, violation_badge
"""

import urllib.parse

import streamlit as st

COLORS = {
    "bg_base": "#C8D0E0",
    "bg_card": "#DDE3EF",
    "bg_soft": "#B8C4D8",
    "bg_empty": "#CCD4E4",
    "border": "#A8B4C8",
    "border_dashed": "#98A6BC",
    "accent": "#5E7BC4",
    "accent_hover": "#4D6AB0",
    "accent_light": "#B4C4E8",
    "accent_mid": "#8FA4D4",
    "peach": "#E8C4BE",
    "peach_soft": "#DFB8B2",
    "mint": "#B8D8CC",
    "mint_border": "#8EC4B0",
    "mint_text": "#1F5E48",
    "mint_sub": "#3D7A62",
    "sky": "#B4D0E8",
    "violation_bg": "#E0B8B4",
    "violation_border": "#C89894",
    "violation_text": "#8B3D38",
    "violation_sub": "#A06058",
    "text_primary": "#1E2430",
    "text_secondary": "#3A4458",
    "text_muted": "#5C687C",
    "text_label": "#4E5A6E",
    "deco": "#6B7A94",
    "grad_accent": "rgba(143, 164, 212, 0.4)",
    "grad_peach": "rgba(232, 196, 190, 0.45)",
    "grad_mint": "rgba(184, 216, 204, 0.38)",
}

# Inline SVG silhouettes for background (scooter + helmet)
_SCOOTER_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 72">'
    '<circle cx="24" cy="54" r="13" fill="none" stroke="{c}" stroke-width="2.2" opacity="0.45"/>'
    '<circle cx="88" cy="54" r="13" fill="none" stroke="{c}" stroke-width="2.2" opacity="0.45"/>'
    '<path d="M24 40 L48 22 L78 18 L102 26 L88 40 Z" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="1.8" opacity="0.5"/>'
    '<path d="M78 18 L84 6 L96 6 L90 18" fill="none" stroke="{c}" stroke-width="1.6" opacity="0.4"/>'
    '<line x1="48" y1="22" x2="42" y2="10" stroke="{c}" stroke-width="1.5" opacity="0.35"/>'
    '</svg>'
)
_HELMET_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 56">'
    '<path d="M32 4C17 4 6 14 4 26h56C58 14 47 4 32 4zm-30 28v6c0 14 11.5 24 26 24s26-10 26-24v-6H2z"'
    ' fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-width="1.6" opacity="0.5"/>'
    '<ellipse cx="32" cy="30" rx="18" ry="6" fill="{c}" fill-opacity="0.08"/>'
    '</svg>'
)


def _bg_deco_layer() -> str:
    """Fixed scooter & helmet silhouettes behind app content."""
    c = COLORS["deco"]
    scooter = _SCOOTER_SVG.format(c=c)
    helmet = _HELMET_SVG.format(c=c)
    items = [
        (scooter, "3%", "5%", "115px", "-14deg", "0.5"),
        (helmet, "10%", "70%", "76px", "10deg", "0.45"),
        (helmet, "76%", "6%", "68px", "-20deg", "0.44"),
        (scooter, "80%", "65%", "100px", "16deg", "0.48"),
        (scooter, "40%", "1%", "85px", "-8deg", "0.35"),
        (helmet, "52%", "85%", "62px", "24deg", "0.4"),
        (helmet, "26%", "35%", "52px", "-28deg", "0.3"),
        (scooter, "65%", "40%", "75px", "18deg", "0.32"),
        (helmet, "88%", "42%", "44px", "12deg", "0.28"),
        (scooter, "1%", "45%", "60px", "-22deg", "0.3"),
    ]
    parts = []
    for svg, left, top, size, rot, op in items:
        parts.append(
            f'<div style="position:absolute;left:{left};top:{top};width:{size};'
            f'opacity:{op};transform:rotate({rot});pointer-events:none;">{svg}</div>'
        )
    return "".join(parts)


def inject_theme():
    c = COLORS
    st.markdown(
        f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Outfit:wght@500;600;700&display=swap');

    :root {{
        --bg-base:         {c["bg_base"]};
        --bg-card:         {c["bg_card"]};
        --bg-soft:         {c["bg_soft"]};
        --border:          {c["border"]};
        --accent:          {c["accent"]};
        --accent-light:    {c["accent_light"]};
        --accent-mid:      {c["accent_mid"]};
        --text-primary:    {c["text_primary"]};
        --text-secondary:  {c["text_secondary"]};
        --text-muted:      {c["text_muted"]};
        --font-display:    'Outfit', sans-serif;
        --font-body:       'DM Sans', sans-serif;
        --radius-lg:       16px;
        --radius-md:       12px;
        --radius-sm:       8px;
        --shadow:          0 2px 8px rgba(30,36,48,0.12), 0 8px 24px rgba(30,36,48,0.08);
        --shadow-md:       0 4px 16px rgba(30,36,48,0.14), 0 12px 32px rgba(30,36,48,0.1);
    }}

    html, body, [class*="css"] {{
        font-family: var(--font-body) !important;
        color: var(--text-primary) !important;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse 75% 50% at 8% 0%, {c["grad_accent"]} 0%, transparent 55%),
            radial-gradient(ellipse 55% 40% at 92% 95%, {c["grad_peach"]} 0%, transparent 50%),
            radial-gradient(ellipse 45% 35% at 50% 55%, {c["grad_mint"]} 0%, transparent 65%),
            {c["bg_base"]} !important;
    }}

    [data-testid="stAppViewContainer"] {{
        position: relative;
        z-index: 1;
    }}

    .block-container {{
        max-width: 920px !important;
        padding: 2rem 1.75rem 3.5rem !important;
        position: relative;
        z-index: 1;
        background: transparent !important;
    }}

    [data-testid="stAppViewContainer"] > section {{
        background: transparent !important;
    }}

    .helmet-bg-wrap {{
        position: fixed !important;
        inset: 0 !important;
        pointer-events: none !important;
        z-index: 0 !important;
        overflow: hidden !important;
    }}

    h1 {{
        font-family: var(--font-display) !important;
        font-size: clamp(1.6rem, 4vw, 2.2rem) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.15rem !important;
    }}

    h2, h3 {{
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }}

    p, li, span, label {{
        font-family: var(--font-body) !important;
        color: var(--text-primary) !important;
    }}

    hr {{
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 1.75rem 0 !important;
    }}

    [data-testid="stFileUploader"] {{
        background: var(--bg-card) !important;
        border: 1.5px dashed var(--accent-mid) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.5rem 1.25rem !important;
        box-shadow: var(--shadow) !important;
        transition: border-color 0.2s, background 0.2s !important;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: var(--accent) !important;
        background: var(--accent-light) !important;
    }}

    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {{
        color: var(--text-secondary) !important;
        font-size: 0.88rem !important;
    }}

    [data-testid="stFileUploader"] button {{
        background: var(--accent-light) !important;
        border: 1px solid var(--accent-mid) !important;
        color: {c["accent_hover"]} !important;
        border-radius: var(--radius-sm) !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }}

    [data-testid="stFileUploader"] button:hover {{
        background: var(--accent) !important;
        color: #fff !important;
        border-color: var(--accent) !important;
    }}

    [data-testid="stCameraInput"] {{
        background: var(--bg-card) !important;
        border: 1.5px dashed var(--accent-mid) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow) !important;
    }}

    [data-testid="stImage"] img {{
        border-radius: var(--radius-md) !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow) !important;
    }}

    [data-testid="stCaptionContainer"] p {{
        color: var(--text-muted) !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.04em !important;
        margin-top: 0.35rem !important;
    }}

    [data-testid="stAlert"],
    div[data-testid="stNotification"] {{
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
    }}

    [data-testid="stSpinner"] {{
        color: var(--accent) !important;
    }}

    [data-testid="stProgress"] > div > div {{
        background: linear-gradient(90deg, {c["accent_mid"]}, {c["accent"]}) !important;
    }}

    [data-testid="stProgress"] > div {{
        background: {c["bg_soft"]} !important;
        border-radius: 99px !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 1.25rem !important;
        align-items: flex-start !important;
    }}

    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg-base); }}
    ::-webkit-scrollbar-thumb {{
        background: var(--accent-mid);
        border-radius: 99px;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>

    <div class="helmet-bg-wrap" aria-hidden="true">{_bg_deco_layer()}</div>

    <div style="
        background: linear-gradient(135deg, {c["bg_card"]} 0%, {c["bg_soft"]} 50%, {c["peach_soft"]} 100%);
        border: 1px solid {c["border"]};
        border-radius: 16px;
        padding: 1.35rem 1.6rem;
        margin-bottom: 1.6rem;
        box-shadow: var(--shadow);
        position: relative;
        z-index: 1;
    ">
        <p style="
            margin:0;
            font-family:'Outfit',sans-serif;
            font-size:0.72rem;
            color:{c["text_label"]};
            letter-spacing:0.12em;
            text-transform:uppercase;
            font-weight:600;
        ">Helmet Detection</p>
        <p style="
            margin:0.4rem 0 0;
            font-family:'DM Sans',sans-serif;
            font-size:0.92rem;
            color:{c["text_secondary"]};
            line-height:1.55;
        ">Upload a file, take a camera photo, or use live webcam to detect helmets and number plates.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def section_card(title: str, icon: str = ""):
    c = COLORS
    st.markdown(
        f"""
    <div style="
        display:flex;
        align-items:center;
        gap:10px;
        margin:1.2rem 0 0.7rem;
        padding:0.55rem 1rem;
        background:{c["bg_card"]};
        border:1px solid {c["border"]};
        border-left:3px solid {c["accent"]};
        border-radius:0 12px 12px 0;
        box-shadow:var(--shadow);
    ">
        <span style="font-size:1.05rem">{icon}</span>
        <span style="
            font-family:'Outfit',sans-serif;
            font-weight:600;
            font-size:0.92rem;
            color:{c["text_primary"]};
        ">{title}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


def violation_badge(detected: bool):
    c = COLORS
    if detected:
        st.markdown(
            f"""
        <div style="
            background:{c["violation_bg"]};
            border:1px solid {c["violation_border"]};
            border-radius:14px;
            padding:1.1rem 1.4rem;
            display:flex;
            align-items:center;
            gap:14px;
            margin-top:0.85rem;
        ">
            <span style="font-size:2rem">🚨</span>
            <div>
                <div style="
                    font-family:'Outfit',sans-serif;
                    font-weight:600;
                    font-size:1.05rem;
                    color:{c["violation_text"]};
                ">Helmet violation detected</div>
                <div style="
                    font-family:'DM Sans',sans-serif;
                    font-size:0.84rem;
                    color:{c["violation_sub"]};
                    margin-top:2px;
                ">Rider is not wearing a helmet.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div style="
            background:{c["mint"]};
            border:1px solid {c["mint_border"]};
            border-radius:14px;
            padding:1.1rem 1.4rem;
            display:flex;
            align-items:center;
            gap:14px;
            margin-top:0.85rem;
        ">
            <span style="font-size:2rem">✅</span>
            <div>
                <div style="
                    font-family:'Outfit',sans-serif;
                    font-weight:600;
                    font-size:1.05rem;
                    color:{c["mint_text"]};
                ">Helmet detected properly</div>
                <div style="
                    font-family:'DM Sans',sans-serif;
                    font-size:0.84rem;
                    color:{c["mint_sub"]};
                    margin-top:2px;
                ">No violation found.</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def plate_card(crop, index: int):
    c = COLORS
    st.markdown(
        f"""
    <div style="
        background:{c["bg_card"]};
        border:1px solid {c["border"]};
        border-radius:12px;
        padding:0.5rem;
        margin-bottom:0.65rem;
        box-shadow:var(--shadow);
    ">
        <p style="
            margin:0 0 0.35rem 0.25rem;
            font-family:'Outfit',sans-serif;
            font-size:0.75rem;
            font-weight:600;
            color:{c["text_muted"]};
            letter-spacing:0.04em;
        ">PLATE #{index}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.image(crop, use_container_width=True)


def processing_indicator():
    c = COLORS
    st.markdown(
        f"""
    <div style="
        display:flex;
        align-items:center;
        gap:10px;
        padding:0.65rem 1rem;
        background:{c["accent_light"]};
        border:1px solid {c["accent_mid"]};
        border-radius:10px;
        margin-bottom:0.85rem;
    ">
        <span style="
            width:8px;height:8px;
            background:{c["accent"]};
            border-radius:50%;
            display:inline-block;
            animation:pulse 1.2s ease-in-out infinite;
        "></span>
        <span style="
            font-family:'DM Sans',sans-serif;
            font-size:0.86rem;
            color:{c["text_secondary"]};
        ">Analyzing frames…</span>
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ opacity:1; transform:scale(1); }}
        50% {{ opacity:0.5; transform:scale(0.85); }}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def empty_state_message():
    """Centered placeholder when no file is uploaded."""
    c = COLORS
    return f"""
    <div style="
        text-align:center;
        padding: 3rem 1rem 2.5rem;
        color: {c["text_muted"]};
        font-family:'DM Sans',sans-serif;
        font-size:0.9rem;
    ">
        <div style="font-size:2.8rem; margin-bottom:0.8rem; opacity:0.6">🛵</div>
        Upload a file, or switch to the Camera / Live webcam tabs.
    </div>
    """


def empty_upload_state():
    st.markdown(empty_state_message(), unsafe_allow_html=True)


def no_plate_placeholder():
    c = COLORS
    st.markdown(
        f"""
    <div style="
        background:{c["bg_empty"]};
        border:1px dashed {c["border_dashed"]};
        border-radius:12px;
        padding:1.2rem;
        text-align:center;
        font-family:'DM Sans',sans-serif;
        font-size:0.82rem;
        color:{c["text_muted"]};
        margin-top:0.4rem;
    ">No plate detected</div>
    """,
        unsafe_allow_html=True,
    )
