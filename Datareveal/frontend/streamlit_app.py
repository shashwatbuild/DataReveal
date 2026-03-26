from __future__ import annotations

import os
from typing import Any, Dict, Optional

import pandas as pd
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="DataReveal", page_icon="AI", layout="wide")

if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_ingest_fp" not in st.session_state:
    st.session_state.last_ingest_fp = None
if "forced_mode" not in st.session_state:
    st.session_state.forced_mode = "auto"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"
if "dark_mode_toggle" not in st.session_state:
    st.session_state.dark_mode_toggle = st.session_state.theme_mode == "dark"


THEMES = {
    "dark": {
        "bg_shell": "radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 28%), radial-gradient(circle at top right, rgba(16, 185, 129, 0.16), transparent 25%), linear-gradient(145deg, #07111f 0%, #0c1729 52%, #132238 100%)",
        "sidebar": "rgba(6, 12, 24, 0.88)",
        "panel": "rgba(9, 19, 34, 0.72)",
        "panel_soft": "rgba(255, 255, 255, 0.04)",
        "panel_border": "rgba(125, 211, 252, 0.18)",
        "text": "#e6f3ff",
        "muted": "#93abc5",
        "accent": "#67e8f9",
        "accent_2": "#34d399",
        "input": "rgba(8, 15, 29, 0.9)",
        "dropzone": "rgba(8, 15, 29, 0.94)",
        "dropzone_text": "#d9ebff",
        "footer": "rgba(5, 10, 20, 0.92)",
        "footer_border": "rgba(125, 211, 252, 0.18)",
        "chat_user": "linear-gradient(135deg, rgba(103, 232, 249, 0.20), rgba(52, 211, 153, 0.16))",
        "chat_assistant": "rgba(15, 23, 42, 0.82)",
        "shadow": "0 24px 60px rgba(2, 6, 23, 0.35)",
        "panel_edge": "inset 0 1px 0 rgba(255,255,255,0.06)",
    },
    "light": {
        "bg_shell": "radial-gradient(circle at top left, rgba(14, 165, 233, 0.16), transparent 28%), radial-gradient(circle at top right, rgba(16, 185, 129, 0.14), transparent 25%), linear-gradient(155deg, #f8fbff 0%, #edf6ff 52%, #dcecff 100%)",
        "sidebar": "rgba(244, 249, 255, 0.9)",
        "panel": "rgba(255, 255, 255, 0.78)",
        "panel_soft": "rgba(255, 255, 255, 0.66)",
        "panel_border": "rgba(14, 165, 233, 0.14)",
        "text": "#0f172a",
        "muted": "#4b6685",
        "accent": "#0284c7",
        "accent_2": "#059669",
        "input": "rgba(255, 255, 255, 0.98)",
        "dropzone": "rgba(255, 255, 255, 0.98)",
        "dropzone_text": "#0f172a",
        "footer": "rgba(239, 247, 255, 0.96)",
        "footer_border": "rgba(14, 165, 233, 0.14)",
        "chat_user": "linear-gradient(135deg, rgba(14, 165, 233, 0.12), rgba(5, 150, 105, 0.10))",
        "chat_assistant": "rgba(255, 255, 255, 0.92)",
        "shadow": "0 20px 55px rgba(15, 23, 42, 0.12)",
        "panel_edge": "inset 0 1px 0 rgba(255,255,255,0.8)",
    },
}


def backend_upload(file) -> Dict[str, Any]:
    files = {"file": (file.name, file.getvalue())}
    r = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
    try:
        r.raise_for_status()
    except Exception:
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = r.text
        raise Exception(f"Backend upload error ({r.status_code}): {detail}")
    return r.json()


def backend_ask(query: str, dataset_id: str, mode: Optional[str] = "auto", top_k: int = 4) -> Dict[str, Any]:
    payload = {"query": query, "dataset_id": dataset_id, "mode": mode, "top_k": top_k}
    r = requests.post(f"{BACKEND_URL}/ask", json=payload, timeout=180)
    try:
        r.raise_for_status()
    except Exception:
        try:
            detail = r.json().get("detail")
        except Exception:
            detail = r.text
        raise Exception(f"Backend ask error ({r.status_code}): {detail}")
    return r.json()


def apply_theme(theme_name: str) -> None:
    theme = THEMES[theme_name]
    st.markdown(
        f"""
        <style>
        :root {{
            --bg-shell: {theme['bg_shell']};
            --sidebar: {theme['sidebar']};
            --panel: {theme['panel']};
            --panel-soft: {theme['panel_soft']};
            --panel-border: {theme['panel_border']};
            --text: {theme['text']};
            --muted: {theme['muted']};
            --accent: {theme['accent']};
            --accent-2: {theme['accent_2']};
            --input: {theme['input']};
            --dropzone: {theme['dropzone']};
            --dropzone-text: {theme['dropzone_text']};
            --footer: {theme['footer']};
            --footer-border: {theme['footer_border']};
            --chat-user: {theme['chat_user']};
            --chat-assistant: {theme['chat_assistant']};
            --shadow: {theme['shadow']};
            --panel-edge: {theme['panel_edge']};
        }}

        html, body, [class*="css"] {{
            color: var(--text);
        }}

        .stApp,
        [data-testid="stAppViewContainer"] {{
            background: var(--bg-shell);
            color: var(--text);
            font-family: "Avenir Next", "Segoe UI", sans-serif;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stSidebar"] {{
            background: var(--sidebar);
            border-right: 1px solid var(--panel-border);
            backdrop-filter: blur(14px);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--text);
        }}

        [data-testid="stSidebarContent"] {{
            padding-bottom: 0.5rem;
            overflow-y: auto;
            overflow-x: hidden;
        }}

        .block-container {{
            max-width: 1180px;
            padding-top: 1.8rem;
            padding-bottom: 2.4rem;
        }}

        h1, h2, h3, p, label, div, span {{
            color: var(--text);
        }}

        .hero-shell {{
            position: relative;
            overflow: hidden;
            padding: 1.55rem;
            border-radius: 28px;
            border: 1px solid var(--panel-border);
            background: linear-gradient(135deg, rgba(103, 232, 249, 0.10), rgba(52, 211, 153, 0.08)), var(--panel);
            box-shadow: var(--shadow), var(--panel-edge);
            transform: perspective(1200px) rotateX(1deg);
            margin-bottom: 1rem;
        }}

        .eyebrow {{
            display: inline-block;
            padding: 0.32rem 0.74rem;
            border-radius: 999px;
            background: rgba(103, 232, 249, 0.12);
            border: 1px solid var(--panel-border);
            color: var(--accent);
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.95rem;
        }}

        .hero-title {{
            margin: 0;
            font-size: clamp(2rem, 4vw, 3.5rem);
            letter-spacing: -0.04em;
            line-height: 0.96;
        }}

        .hero-copy {{
            margin-top: 0.85rem;
            max-width: 760px;
            color: var(--muted);
            font-size: 1rem;
        }}

        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 1rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid var(--panel-border);
            background: var(--panel-soft);
            color: var(--accent-2);
            font-size: 0.88rem;
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
        }}

        .panel {{
            padding: 1rem 1.1rem;
            border-radius: 22px;
            border: 1px solid var(--panel-border);
            background: var(--panel);
            box-shadow: var(--shadow), var(--panel-edge);
            transform: translateZ(0);
            margin-bottom: 1rem;
        }}

        .panel-title {{
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }}

        .panel-copy {{
            color: var(--muted);
            font-size: 0.92rem;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-top: 1rem;
        }}

        .metric-card {{
            padding: 0.95rem;
            border-radius: 20px;
            border: 1px solid var(--panel-border);
            background: var(--panel-soft);
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .metric-value {{
            margin-top: 0.25rem;
            font-size: 1.05rem;
            font-weight: 700;
        }}

        [data-testid="stChatMessage"] {{
            border-radius: 22px;
            border: 1px solid var(--panel-border);
            box-shadow: var(--shadow);
            padding: 0.35rem 0.55rem;
            background: var(--chat-assistant);
        }}

        [data-testid="stBottomBlockContainer"],
        [data-testid="stBottom"] {{
            background: var(--footer) !important;
            border-top: 1px solid var(--footer-border) !important;
        }}

        [data-testid="stChatInput"] {{
            background: transparent !important;
        }}

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInputTextArea"],
        [data-testid="stTextInputRootElement"] input,
        .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stExpander"] {{
            background: var(--input) !important;
            color: var(--text) !important;
            border: 1px solid var(--panel-border) !important;
            border-radius: 18px !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stTextInputRootElement"] input::placeholder {{
            color: var(--muted) !important;
            opacity: 1;
        }}

        [data-testid="stFileUploaderDropzone"] {{
            background: var(--dropzone) !important;
            border: 1px solid var(--panel-border) !important;
            color: var(--dropzone-text) !important;
            border-radius: 20px !important;
        }}

        [data-testid="stFileUploaderDropzone"] * {{
            color: var(--dropzone-text) !important;
        }}

        .stFileUploader > div > div,
        .stFileUploader section {{
            background: transparent !important;
        }}

        .stFileUploader button,
        [data-testid="stFileUploaderDropzone"] button {{
            background: var(--panel-soft) !important;
            color: var(--text) !important;
            border: 1px solid var(--panel-border) !important;
            border-radius: 14px !important;
        }}

        .stButton > button {{
            border-radius: 999px;
            border: 1px solid transparent;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color: white;
            font-weight: 700;
            padding: 0.6rem 1rem;
            box-shadow: 0 12px 28px rgba(14, 165, 233, 0.20);
        }}

        .stAlert {{
            border-radius: 18px;
            border: 1px solid var(--panel-border);
        }}

        code, pre {{
            font-family: "SFMono-Regular", "Menlo", monospace !important;
        }}

        @media (max-width: 900px) {{
            .metric-grid {{
                grid-template-columns: 1fr;
            }}

            .hero-shell {{
                padding: 1.2rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("## Control Deck")
    st.caption("Minimal controls for your data workspace.")
    dark_enabled = st.toggle("Dark mode", key="dark_mode_toggle")
    st.session_state.theme_mode = "dark" if dark_enabled else "light"

apply_theme(st.session_state.theme_mode)

with st.sidebar:
    st.markdown("### Upload data")
    uploaded_file = st.file_uploader(
        "Upload CSV/Excel (SQL) or TXT/PDF (RAG)",
        type=["csv", "xlsx", "xls", "txt", "md", "pdf"],
    )
    if uploaded_file is not None:
        st.caption(f"Selected: {uploaded_file.name}")

    if uploaded_file is not None:
        ingest_fp = f"{uploaded_file.name}:{uploaded_file.size}"
        if st.session_state.dataset_id is None and st.session_state.last_ingest_fp != ingest_fp:
            with st.spinner("Uploading + ingesting (auto)..."):
                try:
                    res = backend_upload(uploaded_file)
                    st.session_state.dataset_id = res.get("dataset_id")
                    st.session_state.last_ingest_fp = ingest_fp
                    st.session_state.messages = []
                    st.success(f"Ingestion complete. dataset_id={st.session_state.dataset_id}")
                    if res.get("mode_ingested"):
                        st.write(f"Mode ingested: `{res.get('mode_ingested')}`")
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")
        elif st.session_state.last_ingest_fp != ingest_fp:
            if st.button("Ingest selected file", disabled=uploaded_file is None, use_container_width=True):
                with st.spinner("Uploading + ingesting..."):
                    try:
                        res = backend_upload(uploaded_file)
                        st.session_state.dataset_id = res.get("dataset_id")
                        st.session_state.last_ingest_fp = ingest_fp
                        st.session_state.messages = []
                        st.success(f"Ingestion complete. dataset_id={st.session_state.dataset_id}")
                        if res.get("mode_ingested"):
                            st.write(f"Mode ingested: `{res.get('mode_ingested')}`")
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")

    st.markdown("### Query mode")
    st.session_state.forced_mode = st.selectbox(
        "Inference route",
        ["auto", "sql", "rag"],
        index=["auto", "sql", "rag"].index(st.session_state.forced_mode),
    )


hero_cols = st.columns([1.6, 1])
with hero_cols[0]:
    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="eyebrow">Neural analytics cockpit</div>
            <h1 class="hero-title">DataReveal</h1>
            <div class="hero-copy">Where your data reveals its story.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_cols[1]:
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">Mission status</div>
            <div class="panel-copy">A focused workspace with cleaner controls and subtle depth.</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Theme</div>
                    <div class="metric-value">{st.session_state.theme_mode.title()}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Mode</div>
                    <div class="metric-value">{st.session_state.forced_mode.upper()}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Dataset</div>
                    <div class="metric-value">{'Ready' if st.session_state.dataset_id else 'Waiting'}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="panel">
        <div class="panel-title">Ask the system</div>
        <div class="panel-copy">Upload structured data for SQL, documents for RAG, or switch routes manually when you want precise control.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question about your uploaded data...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.dataset_id is None:
        with st.chat_message("assistant"):
            st.error(f"Upload a dataset first (backend: {BACKEND_URL}).")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = backend_ask(
                        query=prompt,
                        dataset_id=st.session_state.dataset_id,
                        mode=st.session_state.forced_mode,
                        top_k=4,
                    )
                    answer = res.get("answer", "")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    mode_used = res.get("mode_used")
                    if mode_used == "sql":
                        with st.expander("SQL details"):
                            st.code(res.get("sql", ""), language="sql")
                            preview = res.get("result_preview", {}).get("rows_preview", [])
                            if preview:
                                df = pd.DataFrame(preview)
                                st.dataframe(df, use_container_width=True)
                    elif mode_used == "rag":
                        with st.expander("RAG context"):
                            chunks = res.get("retrieved_context", [])
                            for i, c in enumerate(chunks):
                                meta = c.get("metadata", {})
                                st.write(f"Chunk {i} meta: {meta}")
                                content = c.get("content", "")
                                st.write(content[:1000] + ("..." if len(content) > 1000 else ""))
                except Exception as e:
                    st.error(str(e))
