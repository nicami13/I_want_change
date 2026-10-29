import json
import random
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Cosas lindas que debo decirte",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load_messages():
    messages_path = Path(__file__).with_name("mensajes.json")
    with messages_path.open(encoding="utf-8") as messages_file:
        messages = json.load(messages_file)
    return [message for message in messages if message.get("mensaje")]


messages = load_messages()

if st.session_state.get("app_version") != 2:
    st.session_state.pop("message", None)
    st.session_state.pop("message_id", None)
    st.session_state.app_version = 2

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --ink: #452b35;
        --rose: #a74d62;
        --paper: #fffaf7;
        --muted: #8d7278;
    }

    .stApp {
        color: var(--ink);
        background:
            linear-gradient(180deg, rgba(255, 248, 246, .68), rgba(255, 250, 247, .96) 58%),
            url('https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=2000&q=85') center 28% / cover fixed;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container { max-width: 760px; padding-top: 5.5rem; padding-bottom: 4rem; }

    .eyebrow {
        margin: 0 0 .75rem;
        color: var(--rose);
        font: 600 .72rem 'DM Sans', sans-serif;
        letter-spacing: .16em;
        text-align: center;
        text-transform: uppercase;
    }

    h1 {
        margin: 0 auto .8rem !important;
        max-width: 650px;
        color: var(--ink) !important;
        font: 600 clamp(2.5rem, 7vw, 4.4rem) 'Playfair Display', Georgia, serif !important;
        line-height: 1.08 !important;
        text-align: center;
    }

    .intro {
        margin: 0 auto 2.4rem;
        color: var(--muted);
        font: 400 1rem/1.7 'DM Sans', sans-serif;
        text-align: center;
    }

    [data-testid="stButton"] > div { display: flex; justify-content: center; }
    div.stButton > button {
        min-height: 3.2rem;
        padding: 0 1.55rem;
        border: 1px solid #a74d62;
        border-radius: 999px;
        color: white;
        background: #a74d62;
        font: 600 .94rem 'DM Sans', sans-serif;
        box-shadow: 0 10px 24px rgba(116, 48, 69, .18);
        transition: transform .2s ease, box-shadow .2s ease, background .2s ease;
    }
    div.stButton > button:hover {
        border-color: #893c52;
        color: white;
        background: #893c52;
        box-shadow: 0 13px 28px rgba(116, 48, 69, .23);
        transform: translateY(-2px);
    }
    div.stButton > button:focus:not(:active) {
        color: white;
        border-color: #893c52;
    }

    .message-card {
        margin: 2rem auto 0;
        padding: clamp(1.6rem, 6vw, 3.1rem);
        border: 1px solid rgba(167, 77, 98, .15);
        border-radius: 8px;
        background: rgba(255, 250, 247, .92);
        box-shadow: 0 22px 65px rgba(83, 44, 54, .12);
        text-align: center;
        animation: arrive .55s ease both;
    }
    .message-category {
        margin: 0 0 1rem;
        color: var(--rose);
        font: 600 .7rem 'DM Sans', sans-serif;
        letter-spacing: .15em;
        text-transform: uppercase;
    }
    .message-text {
        margin: 0;
        color: var(--ink);
        font: 500 clamp(1.35rem, 4vw, 2rem)/1.55 'Playfair Display', Georgia, serif;
    }
    .little-heart {
        margin-top: 1.5rem;
        color: var(--rose);
        font-size: 1.1rem;
    }
    .footer-note {
        margin-top: 3.5rem;
        color: #947a80;
        font: 400 .8rem 'DM Sans', sans-serif;
        text-align: center;
    }
    @keyframes arrive {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (max-width: 640px) {
        .block-container { padding: 3.8rem 1.2rem 3rem; }
        .intro { margin-bottom: 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="eyebrow">Una pequeña nota para ti</p>', unsafe_allow_html=True)
st.title("Cosas lindas que debo decirte")
st.markdown(
    '<p class="intro">Hay palabras bonitas esperando su momento. Esta puede ser una.</p>',
    unsafe_allow_html=True,
)

left_space, button_column, right_space = st.columns([1, 1, 1])
with button_column:
    clicked = st.button("Lee tu mensaje", icon=":material/favorite:", type="primary")

if clicked:
    if not messages:
        st.error("Todavía no hay mensajes para mostrar.")
    else:
        previous_id = st.session_state.get("message_id")
        choices = [message for message in messages if message.get("id") != previous_id]
        selected = random.choice(choices or messages)
        st.session_state.message = selected
        st.session_state.message_id = selected.get("id")

if "message" in st.session_state:
    message = st.session_state.message
    st.markdown(
        f"""
        <section class="message-card" aria-live="polite">
            <p class="message-category">{message.get('categoria', 'Para ti')}</p>
            <p class="message-text">{message['mensaje']}</p>
            <div class="little-heart">♥</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<p class="footer-note">Hecho con cariño, solo para ti ♥</p>', unsafe_allow_html=True)