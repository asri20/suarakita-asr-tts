"""
app.py - Aplikasi Utama ASR + TTS Bahasa Indonesia
Streamlit Web Application
"""

import os
import sys
import io
import time
import tempfile
import numpy as np
import streamlit as st


# ── Tambahkan root ke path ─────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Konfigurasi halaman ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SuaraKita — ASR & TTS Bahasa Indonesia",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Custom ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Import Fonts ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ─── Root Variables ────────────────────────────────────────── */
:root {
    --bg-base:      #0A0E1A;
    --bg-surface:   #111827;
    --bg-elevated:  #1C2537;
    --bg-hover:     #243048;
    --border:       #2A3650;
    --accent-blue:  #3B82F6;
    --accent-cyan:  #22D3EE;
    --accent-green: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose:  #F43F5E;
    --text-primary: #F1F5F9;
    --text-muted:   #94A3B8;
    --text-dim:     #64748B;
    --gradient-1:   linear-gradient(135deg, #3B82F6 0%, #22D3EE 100%);
    --gradient-2:   linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
    --gradient-3:   linear-gradient(135deg, #F59E0B 0%, #F43F5E 100%);
    --shadow-lg:    0 20px 60px rgba(0,0,0,0.5);
    --radius:       16px;
}

/* ─── Global ────────────────────────────────────────────────── */
html, body, .stApp {
    background-color: var(--bg-base) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ─── Hide Streamlit chrome ─────────────────────────────────── */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

/* ─── Sidebar ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ─── Typography ────────────────────────────────────────────── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; }

/* ─── Cards ─────────────────────────────────────────────────── */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent-blue); }

.card-gradient {
    background: linear-gradient(135deg, #1C2537 0%, #111827 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px;
    margin-bottom: 20px;
}

/* ─── Hero Banner ───────────────────────────────────────────── */
.hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse 60% 50% at 70% 50%, rgba(59,130,246,0.12) 0%, transparent 70%),
                radial-gradient(ellipse 40% 40% at 20% 80%, rgba(34,211,238,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #F1F5F9 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 12px 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--text-muted);
    margin: 0 0 28px 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.4);
    color: #60A5FA;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    margin-right: 8px;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ─── Metric cards ──────────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.metric-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: var(--accent-blue); }
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label { font-size: 0.8rem; color: var(--text-muted); margin-top: 4px; }

/* ─── Result Display ────────────────────────────────────────── */
.result-box {
    background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(59,130,246,0.1) 100%);
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: var(--radius);
    padding: 28px;
    text-align: center;
    margin: 20px 0;
}
.result-name {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #34D399;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.result-conf {
    font-size: 1rem;
    color: var(--text-muted);
    margin-top: 8px;
}

.demo-notice {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.4);
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 0.85rem;
    color: #FCD34D;
    margin: 12px 0;
}

/* ─── Mic recorder card ─────────────────────────────────────── */
.mic-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(34,211,238,0.08) 100%);
    border: 1.5px solid rgba(59,130,246,0.35);
    border-radius: var(--radius);
    padding: 28px;
    margin-bottom: 20px;
    text-align: center;
}
.mic-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #60A5FA;
    margin-bottom: 6px;
}
.mic-sub {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 18px;
}

/* ─── Buttons ───────────────────────────────────────────────── */
.stButton > button {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ─── Inputs ────────────────────────────────────────────────── */
.stTextArea textarea, .stTextInput input {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
}

/* ─── Selectbox & Radio ─────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ─── Progress / Confidence Bar ─────────────────────────────── */
.conf-bar-container { margin: 6px 0; }
.conf-bar-label {
    display: flex; justify-content: space-between;
    font-size: 0.85rem; color: var(--text-muted);
    margin-bottom: 4px;
}
.conf-bar-track {
    background: var(--bg-elevated);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* ─── Tabs ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-blue) !important;
    color: white !important;
}

/* ─── Divider ────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 24px 0 !important; }

/* ─── File uploader ─────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--bg-elevated) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ─── Audio input (mic recorder) ───────────────────────────── */
[data-testid="stAudioInput"] {
    background: var(--bg-elevated) !important;
    border: 1.5px solid rgba(59,130,246,0.3) !important;
    border-radius: var(--radius) !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Import Modul ───────────────────────────────────────────────────────────────
try:
    from asr import (
        LABELS, SAMPLE_RATE,
        preprocess_bytes, preprocess_audio,
        load_audio_from_bytes,
        extract_mfcc, plot_mfcc, plot_confidence,
        predict_from_bytes, predict_demo, is_model_available,
    )
    ASR_AVAILABLE = True
except ImportError as e:
    ASR_AVAILABLE = False
    ASR_ERROR = str(e)

try:
    from tts import (
        generate_speech_bytes,
        list_voices,
        list_speeds,
        list_volumes,
        get_voice_id,
        get_speed_value,
        get_volume_value,
    )
    TTS_AVAILABLE = True
except ImportError as e:
    TTS_AVAILABLE = False
    TTS_ERROR = str(e)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 8px 0;'>
        <div style='font-size:2.8rem; margin-bottom:8px;'>🎙️</div>
        <div style='font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800;
                    background: linear-gradient(135deg,#3B82F6,#22D3EE);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>SuaraKita</div>
        <div style='font-size:0.75rem; color:#64748B; margin-top:4px;'>
            ASR & TTS Bahasa Indonesia
        </div>
    </div>
    <hr style='border-color:#2A3650; margin:16px 0;'/>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        ["🏠  Beranda", "🎤  Speech Recognition", "🔊  Text-to-Speech", "ℹ️  Tentang Proyek"],
        label_visibility="collapsed",
    )
    page = menu.split("  ")[1]

    st.markdown("<hr style='border-color:#2A3650; margin:20px 0 12px 0;'/>",
                unsafe_allow_html=True)

    # Status modul
    st.markdown("**Status Modul**")
    asr_status = "🟢 Siap" if ASR_AVAILABLE else "🔴 Error"
    tts_status = "🟢 Siap" if TTS_AVAILABLE else "🔴 Error"
    model_status = ("🟢 Tersedia" if (ASR_AVAILABLE and is_model_available())
                    else "🟡 Mode Demo")

    st.markdown(f"""
    <div style='font-size:0.82rem; color:#94A3B8; line-height:2;'>
        ASR Module &nbsp;&nbsp;&nbsp; {asr_status}<br>
        TTS Module &nbsp;&nbsp;&nbsp; {tts_status}<br>
        Model H5 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {model_status}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: Blok hasil prediksi (dipakai di tab Rekam & Upload, agar DRY)
# ══════════════════════════════════════════════════════════════════════════════
def render_prediction(audio_bytes, model_ready):
    """Jalankan prediksi dan tampilkan semua hasil."""
    try:
        audio_np = preprocess_bytes(audio_bytes)

        if model_ready:
            result  = predict_from_bytes(audio_bytes)
            is_demo = False
        else:
            result  = predict_demo(audio_np)
            is_demo = True

        label     = result["label_capitalized"]
        conf      = result["confidence_pct"]
        probs     = result["probabilities"]
        top_k     = result["top_k"]

        # ─── Hasil Prediksi ──────────────────────────────────────
        st.markdown(f"""
        <div class="result-box">
            <div style='font-size:0.85rem; color:#94A3B8;
                        text-transform:uppercase; letter-spacing:0.1em;
                        margin-bottom:8px;'>
                {"⚠️ Mode Demo — " if is_demo else ""}Prediksi Nama
            </div>
            <div class="result-name">{label}</div>
            <div class="result-conf">
                Confidence: <strong style='color:#34D399'>{conf:.1f}%</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ─── Top-K Predictions ───────────────────────────────────
        st.markdown("#### 📊 Confidence Score")
        for i, (lbl, p) in enumerate(top_k):
            pct = p * 100
            bar_color = ("#10B981" if i == 0
                         else "#3B82F6" if i == 1
                         else "#6B7280")
            st.markdown(f"""
            <div class="conf-bar-container">
                <div class="conf-bar-label">
                    <span>{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else '  '} {lbl.capitalize()}</span>
                    <span style='color:#F1F5F9; font-weight:600;'>{pct:.1f}%</span>
                </div>
                <div class="conf-bar-track">
                    <div class="conf-bar-fill"
                         style='width:{pct:.1f}%; background:{bar_color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ─── Visualisasi MFCC ────────────────────────────────────
        st.markdown("#### 🌈 Visualisasi MFCC")
        fig_mfcc = plot_mfcc(
            audio_np,
            title=f"MFCC — Prediksi: {label} ({conf:.1f}%)"
        )
        st.pyplot(fig_mfcc, use_container_width=True)

        # ─── Confidence Bar Chart ────────────────────────────────
        fig_conf = plot_confidence(LABELS, probs)
        st.pyplot(fig_conf, use_container_width=True)

        # ─── Integrasi ke TTS ────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 🔄 Lanjutkan ke TTS")
        if TTS_AVAILABLE:
            tts_text = f"Nama yang terdeteksi adalah {label}"
            if st.button("🔊 Bacakan Hasil Prediksi", use_container_width=True,
                         key=f"tts_btn_{label}_{conf:.0f}"):
                with st.spinner("Membuat audio..."):
                    try:
                        audio_out = generate_speech_bytes(
                            tts_text,
                            voice="id-ID-GadisNeural",
                            rate="+0%"
                        )
                        st.audio(audio_out, format="audio/mp3")
                        st.download_button(
                            "⬇️ Download MP3",
                            data=audio_out,
                            file_name=f"hasil_{label.lower()}.mp3",
                            mime="audio/mpeg",
                            key=f"dl_btn_{label}_{conf:.0f}"
                        )
                    except Exception as e:
                        st.error(f"TTS Error: {e}")
        else:
            st.info("Modul TTS tidak tersedia.")

        # Simpan ke session untuk cross-page
        st.session_state["asr_result"] = label
        st.session_state["asr_text"]   = (f"Nama yang terdeteksi adalah {label}"
                                           if TTS_AVAILABLE else label)

    except Exception as e:
        st.error(f"❌ Error saat memproses: {e}")
        st.exception(e)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if page == "Beranda":
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-title">SuaraKita 🎙️</div>
        <div class="hero-sub">
            Platform ASR & TTS Bahasa Indonesia berbasis Deep Learning.<br>
            Dari suara ke teks, dari teks ke suara — semuanya dalam satu aplikasi.
        </div>
        <span class="hero-badge">🧠 Neural Network</span>
        <span class="hero-badge">🎵 MFCC Features</span>
        <span class="hero-badge">🇮🇩 Bahasa Indonesia</span>
        <span class="hero-badge">⚡ Real-time</span>
        <span class="hero-badge">🔊 edge-tts</span>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">12</div>
            <div class="metric-label">Kelas Nama</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">500+</div>
            <div class="metric-label">Audio Dataset</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">13</div>
            <div class="metric-label">Koefisien MFCC</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">CNN</div>
            <div class="metric-label">Arsitektur Model</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>🎤</div>
            <div style='font-family:Syne,sans-serif; font-size:1.1rem;
                        font-weight:700; margin-bottom:8px;'>
                Automatic Speech Recognition
            </div>
            <div style='color:#94A3B8; font-size:0.9rem; line-height:1.6;'>
                Rekam langsung dari mikrofon atau upload file audio,
                sistem akan mengekstrak fitur MFCC dan memprediksi nama
                menggunakan model CNN 1D yang dilatih dengan dataset Bahasa Indonesia.
            </div>
            <div style='margin-top:16px; font-size:0.8rem; color:#64748B;'>
                ✓ Rekam langsung &nbsp;·&nbsp;
                ✓ Ekstraksi MFCC 13 koefisien &nbsp;·&nbsp;
                ✓ Confidence Score
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>🔊</div>
            <div style='font-family:Syne,sans-serif; font-size:1.1rem;
                        font-weight:700; margin-bottom:8px;'>
                Text-to-Speech
            </div>
            <div style='color:#94A3B8; font-size:0.9rem; line-height:1.6;'>
                Konversi teks Bahasa Indonesia menjadi suara berkualitas tinggi
                menggunakan Microsoft edge-tts dengan pilihan suara pria/wanita,
                kecepatan, dan volume yang dapat disesuaikan.
            </div>
            <div style='margin-top:16px; font-size:0.8rem; color:#64748B;'>
                ✓ Suara Neural ID &nbsp;·&nbsp;
                ✓ Download MP3 &nbsp;·&nbsp;
                ✓ Kecepatan variabel
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Dataset labels
    st.markdown("### 🏷️ Kelas Nama yang Dikenali")
    label_cols = st.columns(6)
    colors = ["#3B82F6", "#22D3EE", "#10B981", "#F59E0B",
              "#F43F5E", "#8B5CF6", "#06B6D4", "#84CC16",
              "#F97316", "#EC4899", "#14B8A6", "#A78BFA"]
    for i, label in enumerate(LABELS):
        with label_cols[i % 6]:
            st.markdown(f"""
            <div style='background:rgba({','.join(str(int(c,16)) for c in
                [colors[i][1:3], colors[i][3:5], colors[i][5:7]])},0.15);
                border:1px solid {colors[i]}60;
                border-radius:10px; padding:10px 8px;
                text-align:center; margin-bottom:10px;
                font-weight:600; font-size:0.9rem;
                color:{colors[i]};'>
                {label.capitalize()}
            </div>
            """, unsafe_allow_html=True)

    # Flow diagram
    st.markdown("### 🔄 Alur Integrasi ASR → TTS")
    st.markdown("""
    <div class="card-gradient" style='text-align:center; padding:32px;'>
        <div style='display:flex; align-items:center; justify-content:center;
                    gap:16px; flex-wrap:wrap; font-size:0.95rem;'>
            <div style='background:#1C2537; border:1px solid #3B82F6;
                        border-radius:12px; padding:14px 20px;'>
                🎙️ <strong>Audio Input</strong><br>
                <span style='font-size:0.78rem; color:#64748B;'>Rekaman / Upload</span>
            </div>
            <div style='color:#3B82F6; font-size:1.5rem;'>→</div>
            <div style='background:#1C2537; border:1px solid #22D3EE;
                        border-radius:12px; padding:14px 20px;'>
                📊 <strong>Preprocessing</strong><br>
                <span style='font-size:0.78rem; color:#64748B;'>Normalisasi & MFCC</span>
            </div>
            <div style='color:#22D3EE; font-size:1.5rem;'>→</div>
            <div style='background:#1C2537; border:1px solid #10B981;
                        border-radius:12px; padding:14px 20px;'>
                🧠 <strong>CNN Model</strong><br>
                <span style='font-size:0.78rem; color:#64748B;'>Prediksi Nama</span>
            </div>
            <div style='color:#10B981; font-size:1.5rem;'>→</div>
            <div style='background:#1C2537; border:1px solid #F59E0B;
                        border-radius:12px; padding:14px 20px;'>
                📝 <strong>Teks Output</strong><br>
                <span style='font-size:0.78rem; color:#64748B;'>Hasil Prediksi</span>
            </div>
            <div style='color:#F59E0B; font-size:1.5rem;'>→</div>
            <div style='background:#1C2537; border:1px solid #F43F5E;
                        border-radius:12px; padding:14px 20px;'>
                🔊 <strong>TTS Output</strong><br>
                <span style='font-size:0.78rem; color:#64748B;'>edge-tts Audio</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ASR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Speech Recognition":
    st.markdown("""
    <div style='margin-bottom:8px;'>
        <span class='hero-badge'>🤖 CNN 1D Model</span>
        <span class='hero-badge'>🎵 MFCC Features</span>
        <span class='hero-badge'>🎙️ Real-time Mic</span>
    </div>
    <h1 style='font-family:Syne,sans-serif; font-size:2.2rem; margin:0 0 8px 0;'>
        🎤 Automatic Speech Recognition
    </h1>
    <p style='color:#94A3B8; font-size:1rem; margin-bottom:28px;'>
        Rekam langsung dari mikrofon atau upload file audio WAV — sistem akan memprediksi
        nama menggunakan Neural Network berbasis fitur MFCC.
    </p>
    """, unsafe_allow_html=True)

    if not ASR_AVAILABLE:
        st.error(f"❌ Modul ASR tidak tersedia: {ASR_ERROR}")
        st.stop()

    # Cek model
    model_ready = is_model_available()
    if not model_ready:
        st.markdown("""
        <div class="demo-notice">
            ⚠️ <strong>Mode Demo Aktif</strong> — File <code>asr/model/model_asr.h5</code> belum ditemukan.
            Prediksi menggunakan model random (tidak akurat). Lakukan training di Google Colab
            dan letakkan model di <code>asr/model/model_asr.h5</code> untuk hasil nyata.
        </div>
        """, unsafe_allow_html=True)

    # ── 3 Tab: Rekam | Upload | Panduan ───────────────────────────────────────
    tab_mic, tab_upload, tab_info = st.tabs([
        "🎙️ Rekam Langsung",
        "📂 Upload Audio",
        "📋 Panduan Dataset",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1 — REKAM LANGSUNG
    # ─────────────────────────────────────────────────────────────────────────
    with tab_mic:
        col_main, col_side = st.columns([3, 2])

        with col_main:
            st.markdown("""
            <div class="mic-card">
                <div class="mic-title">🎙️ Rekam Suara dari Mikrofon</div>
                <div class="mic-sub">
                    Klik tombol mikrofon di bawah → ucapkan nama → klik stop.<br>
                    Sistem langsung memprediksi nama yang diucapkan.
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Komponen perekam bawaan Streamlit ─────────────────────────────
            audio_recorded = st.audio_input(
                "Klik 🎙️ untuk mulai rekam, klik ⏹️ untuk stop",
                key="mic_recorder",
            )

            if audio_recorded is not None:
                audio_bytes = audio_recorded.read()

                # Putar ulang rekaman
                st.markdown("**▶️ Rekaman kamu:**")
                st.audio(audio_bytes, format="audio/wav")

                # Tombol analisis
                if st.button("🚀 Analisis & Prediksi", type="primary",
                             use_container_width=True, key="btn_predict_mic"):
                    with st.spinner("Memproses audio..."):
                        render_prediction(audio_bytes, model_ready)
            else:
                st.markdown("""
                <div style='background:#1C2537; border:1px dashed #2A3650;
                            border-radius:12px; padding:32px; text-align:center;
                            color:#64748B; font-size:0.9rem; margin-top:8px;'>
                    🎙️ Belum ada rekaman.<br>
                    <span style='font-size:0.8rem;'>
                        Klik tombol mikrofon di atas untuk mulai merekam.
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with col_side:
            st.markdown("#### ℹ️ Kelas yang Didukung")
            for lbl in LABELS:
                st.markdown(f"""
                <div style='background:#1C2537; border:1px solid #2A3650;
                            border-radius:8px; padding:8px 14px; margin-bottom:6px;
                            font-size:0.9rem;'>
                    📌 {lbl.capitalize()}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 💡 Tips Rekam")
            st.markdown("""
            <div class="card" style='padding:16px;'>
                <div style='font-size:0.85rem; color:#94A3B8; line-height:1.8;'>
                    ✅ Izinkan akses mikrofon di browser<br>
                    ✅ Rekam di tempat senyap<br>
                    ✅ Durasi cukup 1–2 detik<br>
                    ✅ Ucapkan nama dengan jelas<br>
                    ✅ Jarak mikrofon ±20–30 cm
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2 — UPLOAD FILE
    # ─────────────────────────────────────────────────────────────────────────
    with tab_upload:
        col_main, col_side = st.columns([3, 2])

        with col_main:
            st.markdown("#### 📂 Upload File Audio")
            uploaded = st.file_uploader(
                "Pilih file audio WAV (16kHz, 1–2 detik)",
                type=["wav", "WAV", "mp3", "ogg"],
                help="Format terbaik: WAV mono 16kHz. Ucapkan salah satu dari 12 nama yang tersedia.",
                key="file_uploader",
            )

            if uploaded:
                audio_bytes = uploaded.read()
                st.audio(audio_bytes, format="audio/wav")

                if st.button("🚀 Analisis & Prediksi", type="primary",
                             use_container_width=True, key="btn_predict_upload"):
                    with st.spinner("Memproses audio..."):
                        render_prediction(audio_bytes, model_ready)
            else:
                st.markdown("""
                <div style='background:#1C2537; border:1px dashed #2A3650;
                            border-radius:12px; padding:32px; text-align:center;
                            color:#64748B; font-size:0.9rem; margin-top:8px;'>
                    📂 Belum ada file dipilih.<br>
                    <span style='font-size:0.8rem;'>
                        Klik "Browse files" di atas untuk upload file audio.
                    </span>
                </div>
                """, unsafe_allow_html=True)

        with col_side:
            st.markdown("#### ℹ️ Kelas yang Didukung")
            for lbl in LABELS:
                st.markdown(f"""
                <div style='background:#1C2537; border:1px solid #2A3650;
                            border-radius:8px; padding:8px 14px; margin-bottom:6px;
                            font-size:0.9rem;'>
                    📌 {lbl.capitalize()}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 💡 Tips Upload")
            st.markdown("""
            <div class="card" style='padding:16px;'>
                <div style='font-size:0.85rem; color:#94A3B8; line-height:1.8;'>
                    ✅ Gunakan mikrofon berkualitas<br>
                    ✅ Rekam di tempat senyap<br>
                    ✅ Durasi 1–2 detik<br>
                    ✅ Sample rate 16000 Hz<br>
                    ✅ Format WAV mono
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3 — PANDUAN DATASET
    # ─────────────────────────────────────────────────────────────────────────
    with tab_info:
        st.markdown("""
        ### 📁 Struktur Dataset
        Dataset berisi rekaman audio 12 nama dalam Bahasa Indonesia.
        """)
        st.code("""
dataset/
├── yesus/         (40-50 file .wav)
├── simon/         (40-50 file .wav)
├── andreas/       (40-50 file .wav)
├── yakobus/       (40-50 file .wav)
├── yohanes/       (40-50 file .wav)
├── filipus/       (40-50 file .wav)
├── bartomeleus/   (40-50 file .wav)
├── tomas/         (40-50 file .wav)
├── matius/        (40-50 file .wav)
├── tadeus/        (40-50 file .wav)
├── yudas/         (40-50 file .wav)
└── maria/         (40-50 file .wav)
        """, language="text")

        st.markdown("""
        ### 🧠 Arsitektur Model CNN 1D
        """)
        st.code("""
Input: (batch, 32, 13)   # (batch, MAX_LEN, N_MFCC)
  ↓
Conv1D(32, kernel=3, activation='relu', padding='same')
MaxPooling1D(pool_size=2)
  ↓
Conv1D(64, kernel=3, activation='relu', padding='same')
MaxPooling1D(pool_size=2)
  ↓
Flatten()
Dense(128, activation='relu')
Dropout(0.3)
  ↓
Dense(12, activation='softmax')  # 12 kelas nama

Optimizer: Adam
Loss: sparse_categorical_crossentropy
        """, language="text")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Text-to-Speech":
    st.markdown("""
    <div style='margin-bottom:8px;'>
        <span class='hero-badge'>🔊 edge-tts</span>
        <span class='hero-badge'>🌍 Multilingual Neural Voice</span>
    </div>
    <h1 style='font-family:Syne,sans-serif; font-size:2.2rem; margin:0 0 8px 0;'>
        🔊 Text-to-Speech
    </h1>
    <p style='color:#94A3B8; font-size:1rem; margin-bottom:28px;'>
        Konversi teks Bahasa Indonesia menjadi suara natural menggunakan
        Microsoft Neural TTS multilingual. Pilih berbagai voice internasional dengan pengaturan kecepatan dan volume yang fleksibel.
    </p>
    """, unsafe_allow_html=True)

    if not TTS_AVAILABLE:
        st.error(f"❌ Modul TTS tidak tersedia: {TTS_ERROR}")
        st.stop()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Cek apakah ada hasil ASR untuk dipakai
        asr_text = st.session_state.get("asr_text", "")

        st.markdown("#### ✏️ Input Teks")
        if asr_text:
            st.markdown("""
            <div style='background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3);
                        border-radius:8px; padding:10px 14px; margin-bottom:12px;
                        font-size:0.85rem; color:#34D399;'>
                ✅ Hasil ASR tersedia — teks di bawah diisi dari prediksi ASR
            </div>
            """, unsafe_allow_html=True)

        text_input = st.text_area(
            "Masukkan teks yang ingin diucapkan:",
            value=asr_text if asr_text else "Halo, selamat datang di aplikasi SuaraKita. Aplikasi ini menggunakan teknologi pengenalan suara dan sintesis suara berbahasa Indonesia.",
            height=160,
            placeholder="Ketik teks Bahasa Indonesia di sini...",
            label_visibility="collapsed",
        )

        char_count = len(text_input)
        st.caption("🌍 Mendukung Bahasa Indonesia, English, Japanese, dan Korean")
        st.markdown(f"""
        <div style='text-align:right; font-size:0.8rem; color:#64748B; margin:-12px 0 16px 0;'>
            {char_count} karakter
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎵 Generate Suara", type="primary", use_container_width=True):
            if not text_input.strip():
                st.warning("⚠️ Teks tidak boleh kosong!")
            else:
                with st.spinner("Menghasilkan audio... ⏳"):
                    try:
                        voice_id   = st.session_state.get("tts_voice", "id-ID-GadisNeural")
                        speed_val  = st.session_state.get("tts_speed", "+0%")
                        volume_val = st.session_state.get("tts_volume", "+0%")

                        audio_bytes = generate_speech_bytes(
                            text_input,
                            voice=voice_id,
                            rate=speed_val,
                            volume=volume_val,
                        )

                        st.markdown("""
                        <div style='background:rgba(16,185,129,0.1);
                                    border:1px solid rgba(16,185,129,0.3);
                                    border-radius:12px; padding:20px;
                                    margin:16px 0;'>
                            <div style='font-weight:600; color:#34D399; margin-bottom:12px;'>
                                ✅ Audio berhasil dibuat!
                            </div>
                        """, unsafe_allow_html=True)

                        st.audio(audio_bytes, format="audio/mp3")

                        dl_name = f"tts_{int(time.time())}.mp3"
                        st.download_button(
                            "⬇️ Download MP3",
                            data=audio_bytes,
                            file_name=dl_name,
                            mime="audio/mpeg",
                            use_container_width=True,
                        )
                        st.markdown("</div>", unsafe_allow_html=True)

                        st.session_state["tts_last_audio"] = audio_bytes
                        st.session_state["tts_last_text"]  = text_input

                    except Exception as e:
                        st.error(f"❌ Gagal generate audio: {e}")
                        st.exception(e)

    with col_right:
        st.markdown("#### ⚙️ Pengaturan Suara")

        # Voice selection
        voice_names = list_voices()

        selected_voice_name = st.selectbox(
            "🌍 Pilih Voice",
            voice_names,
            index=0,
            help="Pilih voice multilingual neural"
        )

        voice_id = get_voice_id(selected_voice_name)
        st.session_state["tts_voice"] = voice_id

        # Gender badge
        if "Female" in selected_voice_name or "Perempuan" in selected_voice_name:
            badge_color = "#EC4899"
            badge_icon  = "♀️"
        else:
            badge_color = "#3B82F6"
            badge_icon  = "♂️"
        st.markdown(f"""
        <div style='background:rgba(0,0,0,0.2); border:1px solid {badge_color}50;
                    border-radius:8px; padding:8px 14px; margin-bottom:16px;
                    font-size:0.85rem; color:{badge_color};'>
            {badge_icon} Neural Voice: <code style='color:{badge_color}'>{voice_id}</code>
        </div>
        """, unsafe_allow_html=True)

        # Speed
        speed_names = list_speeds()
        selected_speed = st.selectbox("⚡ Kecepatan Bicara", speed_names, index=1)
        speed_val = get_speed_value(selected_speed)
        st.session_state["tts_speed"] = speed_val

        # Volume
        volume_names = list_volumes()
        selected_volume = st.selectbox("🔉 Volume", volume_names, index=1)
        volume_val = get_volume_value(selected_volume)
        st.session_state["tts_volume"] = volume_val

        # Settings preview
        st.markdown(f"""
        <div class="card" style='padding:16px; margin-top:4px;'>
            <div style='font-size:0.82rem; font-weight:600;
                        color:#94A3B8; margin-bottom:10px;'>
                Konfigurasi Aktif
            </div>
            <div style='font-size:0.85rem; line-height:2; color:#E2E8F0;'>
                🎤 Suara &nbsp;&nbsp;&nbsp; <code>{voice_id}</code><br>
                ⚡ Rate &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <code>{speed_val}</code><br>
                🔉 Volume &nbsp; <code>{volume_val}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Contoh teks
        st.markdown("#### 💬 Contoh Teks")
        examples = [
            "Halo, nama saya Maria.",
            "Selamat pagi, hari ini cuacanya cerah.",
            "Hello everyone, welcome to SuaraKita.",
            "Artificial intelligence is amazing.",
            "こんにちは、元気ですか？",
            "안녕하세요, 만나서 반갑습니다.",
        ]
        for ex in examples:
            if st.button(f'"{ex[:35]}..."' if len(ex) > 35 else f'"{ex}"',
                         use_container_width=True):
                st.session_state["tts_example"] = ex
                st.rerun()

        if "tts_example" in st.session_state:
            st.info(f"💡 Salin teks: *{st.session_state['tts_example']}*")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Tentang Proyek":
    st.markdown("""
    <h1 style='font-family:Syne,sans-serif; font-size:2.2rem; margin:0 0 8px 0;'>
        ℹ️ Tentang Proyek
    </h1>
    <p style='color:#94A3B8; margin-bottom:28px;'>
        Proyek akhir berbasis Deep Learning — ASR & TTS Bahasa Indonesia
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>🧠</div>
            <div style='font-family:Syne,sans-serif; font-weight:700;
                        font-size:1.05rem; margin-bottom:12px;'>Teknologi ASR</div>
            <div style='font-size:0.875rem; color:#94A3B8; line-height:1.9;'>
                🔹 <strong>Librosa</strong> — Ekstraksi fitur MFCC<br>
                🔹 <strong>TensorFlow/Keras</strong> — Training model CNN<br>
                🔹 <strong>NumPy</strong> — Komputasi numerik<br>
                🔹 <strong>scikit-learn</strong> — Evaluasi model<br>
                🔹 <strong>Matplotlib</strong> — Visualisasi MFCC<br>
                🔹 <strong>soundfile</strong> — I/O file audio<br>
                🔹 <strong>Google Colab</strong> — Platform training
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>📊</div>
            <div style='font-family:Syne,sans-serif; font-weight:700;
                        font-size:1.05rem; margin-bottom:12px;'>Pipeline ASR</div>
            <div style='font-size:0.875rem; color:#94A3B8; line-height:2;'>
                1️⃣ Input audio (Mikrofon / WAV 16kHz)<br>
                2️⃣ Normalisasi & Trim silence<br>
                3️⃣ Pad/Truncate ke 2 detik<br>
                4️⃣ Ekstraksi MFCC (13 koef, 32 frame)<br>
                5️⃣ Inferensi CNN 1D model<br>
                6️⃣ Output: nama + confidence score
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>🔊</div>
            <div style='font-family:Syne,sans-serif; font-weight:700;
                        font-size:1.05rem; margin-bottom:12px;'>Teknologi TTS</div>
            <div style='font-size:0.875rem; color:#94A3B8; line-height:1.9;'>
                🔹 <strong>edge-tts</strong> — Microsoft Neural TTS<br>
                🔹 <strong>asyncio</strong> — Async audio generation<br>
                🔹 <strong>pydub</strong> — Audio processing<br>
                🔹 <strong>id-ID-GadisNeural</strong> — Suara wanita<br>
                🔹 <strong>id-ID-ArdiNeural</strong> — Suara pria<br>
                🔹 Format output: MP3
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div style='font-size:1.8rem; margin-bottom:12px;'>🏗️</div>
            <div style='font-family:Syne,sans-serif; font-weight:700;
                        font-size:1.05rem; margin-bottom:12px;'>Struktur Proyek</div>
            <div style='font-size:0.8rem; color:#94A3B8;'>
        """, unsafe_allow_html=True)
        st.code("""
speech-app/
├── app.py               # Main Streamlit app
├── requirements.txt
├── asr/
│   ├── preprocess.py    # Audio preprocessing
│   ├── feature_extraction.py  # MFCC
│   ├── predict.py       # Model inference
│   ├── utils.py         # Utilities
│   ├── model/
│   │   └── model_asr.h5
│   └── training/
│       └── asr_training.ipynb
└── tts/
    ├── generate.py      # edge-tts wrapper
    ├── voices.py        # Voice config
    └── audio_output/
        """, language="text")
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Dataset info
    st.markdown("""
    <div class="card" style='margin-top:8px;'>
        <div style='font-size:1.8rem; margin-bottom:12px;'>🗂️</div>
        <div style='font-family:Syne,sans-serif; font-weight:700;
                    font-size:1.05rem; margin-bottom:16px;'>Spesifikasi Dataset</div>
        <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:16px;'>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#3B82F6; font-family:Syne,sans-serif;'>12</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Kelas Nama</div>
            </div>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#10B981; font-family:Syne,sans-serif;'>500+</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Total Audio</div>
            </div>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#F59E0B; font-family:Syne,sans-serif;'>16kHz</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Sample Rate</div>
            </div>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#8B5CF6; font-family:Syne,sans-serif;'>1–2s</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Durasi Audio</div>
            </div>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#22D3EE; font-family:Syne,sans-serif;'>WAV</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Format File</div>
            </div>
            <div style='background:#1C2537; border-radius:10px; padding:14px; text-align:center;'>
                <div style='font-size:1.5rem; font-weight:800;
                            color:#F43F5E; font-family:Syne,sans-serif;'>CNN</div>
                <div style='font-size:0.8rem; color:#94A3B8; margin-top:4px;'>Model Arsitektur</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # GitHub
    st.markdown("""
    <div class="card" style='text-align:center; margin-top:8px;'>
        <div style='font-size:1.8rem; margin-bottom:12px;'>🐙</div>
        <div style='font-family:Syne,sans-serif; font-weight:700; font-size:1.05rem;
                    margin-bottom:8px;'>Version Control</div>
        <div style='color:#94A3B8; font-size:0.9rem; margin-bottom:16px;'>
            Proyek ini dikelola menggunakan GitHub untuk kolaborasi tim.
        </div>
        <code style='background:#1C2537; border:1px solid #2A3650;
                     border-radius:8px; padding:8px 16px; font-size:0.9rem;
                     color:#58A6FF;'>
            git clone https://github.com/[username]/speech-app.git
        </code>
    </div>
    """, unsafe_allow_html=True)