"""
SuaraKita — AI Voice Platform
Clean Dark Theme Redesign (Preserving Full Backend & UI Features)
"""

import os, sys, time
import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SuaraKita — AI Voice Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS — graceful fallback jika modul belum ada
# ══════════════════════════════════════════════════════════════════════════════
try:
    from asr import (
        LABELS, SAMPLE_RATE, preprocess_bytes, preprocess_audio,
        load_audio_from_bytes, extract_mfcc, plot_mfcc, plot_confidence,
        predict_from_bytes, predict_demo, is_model_available,
    )
    ASR_OK = True; ASR_ERR = ""
except ImportError as e:
    ASR_OK = False; ASR_ERR = str(e)
    LABELS = ["yesus","simon","andreas","yakobus","yohanes","filipus",
              "bartomeleus","tomas","matius","tadeus","yudas","maria"]

try:
    from tts import (
        generate_speech_bytes, list_voices, list_speeds, list_volumes,
        get_voice_id, get_speed_value, get_volume_value,
    )
    TTS_OK = True; TTS_ERR = ""
except ImportError as e:
    TTS_OK = False; TTS_ERR = str(e)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS - CLEAN DARK MODE (Like Screenshot)
# ══════════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Clean Dark Palette from Screenshots */
  --bg-main: #0F0A1F;
  --bg-card: #18122B;
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(255, 255, 255, 0.2);
  
  --primary: #8B5CF6;
  --secondary: #A855F7;
  --accent: #EC4899;

  --green: #10B981;

  --grad: linear-gradient(
  135deg,
  #8B5CF6 0%,
  #A855F7 50%,
  #EC4899 100%
  );
    
  --text: #F9FAFB;
  --text-muted: #9CA3AF;
  --text-dim: #4B5563;
}

/* ── Base ── */
html, body, .stApp {
  background: var(--bg-main) !important;
  font-family: 'Inter', sans-serif !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header, [data-testid="stDecoration"] { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 1200px !important; margin: 0 auto; }
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* ── Main wrapper ── */
.wrap {
  position: relative; z-index: 1; padding: 0 28px 100px;
}

/* ══════════════════════════════════════════════════════════
   TOP NAV
══════════════════════════════════════════════════════════ */
.topnav {
  position: sticky; top: 0; z-index: 200;
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.2rem 0; border-bottom: 1px solid var(--border-subtle);
  background: rgba(11, 16, 30, 0.95);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
}
.logo-wrap { display: flex; align-items: center; gap: 11px; }
.logo-icon {
  width: 32px; height: 32px; border-radius: 8px;
  background: var(--grad); display: flex; align-items: center; justify-content: center;
  font-size: 1rem; color: white;
}
.logo-name {
  font-size: 1.2rem; font-weight: 700; letter-spacing: -0.5px;
}
.nav-pills { display: flex; gap: 15px; }
.nav-pill {
  padding: 6px 12px; border-radius: 6px; font-size: 0.9rem; font-weight: 500;
  color: var(--text-muted); transition: 0.2s; border: 1px solid transparent;
}
.nav-pill.active {
  color: var(--sky); background: rgba(56,189,248,.08); border-color: rgba(56,189,248,.2);
}
.nav-status {
  display: flex; gap: 7px; align-items: center; font-size: 0.75rem; 
  font-weight: 600; letter-spacing: 1px; color: var(--text-muted); text-transform: uppercase;
}
.status-dot {
  width: 8px; height: 8px; border-radius: 50%; background: var(--green);
}

/* ══════════════════════════════════════════════════════════
   HERO
══════════════════════════════════════════════════════════ */
.hero { text-align: center; padding: 4rem 0 2rem; position: relative; }
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px;
  border-radius: 999px; background: rgba(139,92,246,.1);
  border: 1px solid rgba(56,189,248,.2); color: #A855F7;; 
  font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; 
  margin-bottom: 2rem;
}
.hero-h1 {
  font-size: clamp(2.5rem, 5vw, 4rem); font-weight: 800; line-height: 1.1; margin: 0 0 1rem; letter-spacing: -1px;
}
.hero-h1-grad {
  background: var(--grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 1.05rem; color: var(--text-muted); max-width: 650px; margin: 0 auto 2.5rem; line-height: 1.6;
}

/* Buttons for CTA */
.hero-cta { display:flex; justify-content:center; gap:15px; margin-bottom: 2rem; }
.cta-btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px;
  border-radius: 8px; background: transparent; border: 1px solid var(--border-hover);
  color: var(--text); font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: 0.3s;
}
.cta-btn:hover { border-color: white; background: rgba(255,255,255,0.05); }

/* Static Waveform from screenshot */
.hero-wave { display: flex; align-items: center; justify-content: center; gap: 4px; height: 60px; margin: 2rem auto; }
.wv-bar { width: 4px; border-radius: 4px; background: var(--grad); opacity: 0.8; }

.down-arrow {
  width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--border-subtle);
  display: flex; align-items: center; justify-content: center; background: var(--bg-card);
  color: var(--text-muted); margin: 0 auto; transition: 0.3s;
}

/* ══════════════════════════════════════════════════════════
   STATS STRIP
══════════════════════════════════════════════════════════ */
.stats-strip {
  display: grid; grid-template-columns: repeat(4, 1fr);
  background: var(--bg-card); border: 1px solid var(--border-subtle); 
  border-radius: 16px; margin: 3rem 0;
}
.stat-cell {
  padding: 2.5rem 1rem; text-align: center; border-right: 1px solid var(--border-subtle);
}
.stat-cell:last-child { border-right: none; }
.stat-val {
  font-size: 2.5rem; font-weight: 800; background: var(--grad); 
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; line-height: 1;
}
.stat-lbl { font-size: 0.8rem; font-weight: 600; color: var(--text-dim); letter-spacing: 1.5px; text-transform: uppercase; }

/* ══════════════════════════════════════════════════════════
   GLASS CARDS (Now flat clean cards)
══════════════════════════════════════════════════════════ */
.gc {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: 16px; padding: 24px; transition: 0.3s; height: 100%;
}
.gc:hover { border-color: var(--border-hover); }
.gc-accent {
  background: var(--bg-card); border: 1px solid var(--border-subtle); 
  border-radius: 16px; padding: 24px; height: 100%;
}

/* Feature tags inside cards */
.tech-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px; }
.tech-tag-blue {
  padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
  background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.2); color: var(--sky);
}
.tech-tag-purple {
  padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
  background: rgba(129, 140, 248, 0.1); border: 1px solid rgba(129, 140, 248, 0.2); color: var(--purple);
}

/* Typography elements */
.sec-eyebrow {
  font-size: 0.75rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--sky); margin-bottom: 0.5rem;
}
.sec-title {
  font-size: 1.75rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem; letter-spacing: -0.5px;
}
.sec-desc { font-size: 0.95rem; color: var(--text-muted); margin-bottom: 2rem; }
.sec-divider { height: 1px; background: var(--border-subtle); margin: 3rem 0; }

/* ══════════════════════════════════════════════════════════
   PREDICTION CARD
══════════════════════════════════════════════════════════ */
.pred-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle); 
  border-radius: 16px; padding: 2rem; text-align: center;
}
.pred-label   { font-size: 0.8rem; font-weight: 600; color: var(--text-muted); margin-bottom: 10px; }
.pred-name    { font-size: 2.5rem; font-weight: 800; color: #A855F7; text-transform: uppercase; margin-bottom: 10px; }
.pred-conf    { font-size: 1rem; color: var(--text-muted); }
.pred-conf strong { color: var(--green); }

/* Confidence Bars */
.conf-row     { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.conf-rank    { display:none; } /* Hidden for cleaner look */
.conf-name    { font-size: 0.85rem; color: var(--text-muted); width: 80px; text-transform: capitalize; }
.conf-track   { flex: 1; height: 6px; background: rgba(255,255,255,0.05); border-radius: 4px; overflow: hidden; }
.conf-fill    { height: 100%; background: var(--grad); border-radius: 4px; }
.conf-pct     { font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; color: var(--text-muted); width: 45px; text-align: right; }

/* ══════════════════════════════════════════════════════════
   LABEL GRID
══════════════════════════════════════════════════════════ */
.label-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 10px; margin-top: 10px; }
.label-chip {
  padding: 8px 12px; border-radius: 8px; text-align: center;
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  font-size: 0.85rem; font-weight: 500; color: var(--text-muted);
}
.label-chip.active {
  background: rgba(16,185,129,.1); border-color: var(--green); color: var(--green);
}

/* ══════════════════════════════════════════════════════════
   PIPELINE
══════════════════════════════════════════════════════════ */
.pipeline { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 1rem 0; overflow-x: auto;}
.pipe-node {
  display: flex; flex-direction: column; align-items: center; text-align: center; width: 120px;
}
.pipe-icon {
  width: 45px; height: 45px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid var(--border-subtle);
  display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-bottom: 10px;
}
.pipe-title { font-size: 0.85rem; font-weight: 600; color: var(--text); }
.pipe-sub   { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }
.pipe-connector { flex: 1; height: 1px; background: var(--border-subtle); margin-bottom: 30px; }
.pipe-node.active .pipe-icon { background: rgba(56,189,248,.1); border-color: var(--sky); color: var(--sky); }

/* ══════════════════════════════════════════════════════════
   STREAMLIT OVERRIDES (Matched to Screenshot UI)
══════════════════════════════════════════════════════════ */
.stButton > button {
  background: transparent !important; color: white !important; border: 1px solid var(--border-hover) !important;
  border-radius: 8px !important; font-weight: 600 !important; font-size: 0.95rem !important;
  padding: 0.75rem 1.5rem !important; transition: 0.3s !important; width: 100%;
}
.stButton > button:hover { background: rgba(255,255,255,0.05) !important; border-color: white !important; }

.stTextArea textarea {
  background: var(--bg-card) !important; border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important; color: var(--text) !important; padding: 1rem !important; font-size: 0.95rem !important;
}
.stTextArea textarea:focus { border-color: var(--sky) !important; }
.stTextArea label, .stSelectbox label { color: var(--text-muted) !important; font-size: 0.85rem !important; }

.stSelectbox > div > div {
  background: var(--bg-card) !important; border: 1px solid var(--border-subtle) !important;
  border-radius: 8px !important; color: var(--text) !important;
}

[data-testid="stFileUploader"] {
  background: var(--bg-card) !important; border: 1px dashed var(--border-hover) !important; border-radius: 12px !important;
}
[data-testid="stFileUploader"] * { color: var(--text-muted) !important; }

[data-testid="stAudioInput"] {
  background: var(--bg-card) !important; border: 1px solid var(--border-subtle) !important; border-radius: 12px !important;
}

.stTabs [data-baseweb="tab-list"] {
  background: transparent !important; border-bottom: 1px solid var(--border-subtle) !important; gap: 20px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border: none !important; color: var(--text-muted) !important;
  font-weight: 500 !important; padding: 10px 0 !important; border-bottom: 2px solid transparent !important; border-radius: 0 !important;
}
.stTabs [aria-selected="true"] {
  color: var(--sky) !important; border-bottom: 2px solid var(--sky) !important;
}
.stTabs [data-testid="stTabContent"] { padding: 20px 0 0 !important; }

.demo-warn {
  display: flex; gap: 10px; background: rgba(245,158,11,.1); border: 1px solid rgba(245,158,11,.3);
  padding: 12px 16px; border-radius: 8px; color: #FCD34D; font-size: 0.85rem; margin-bottom: 20px;
}
</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS (Preserving Backend & Features)
# ══════════════════════════════════════════════════════════════════════════════
def render_waveform():
    """Renders the static clean waveform like the screenshot."""
    heights = [8, 12, 8, 12, 16, 12, 18, 24, 30, 40, 50, 60, 50, 40, 30, 24, 18, 12, 16, 12, 8, 12, 8]
    bars = "".join([f'<div class="wv-bar" style="height: {h}px;"></div>' for h in heights])
    return f'<div class="hero-wave">{bars}</div>'

def render_confidence_bars(top_k):
    colors = colors = [
    "#8B5CF6",
    "#A855F7",
    "#EC4899",
    "#C084FC",
    "#F472B6"
]
    html = '<div style="margin-top:20px;">'
    for i, (lbl, p) in enumerate(top_k):
        c = colors[i] if i < 5 else "#4B5563"
        pct = p * 100
        html += f"""
        <div class="conf-row">
          <div class="conf-name">{lbl}</div>
          <div class="conf-track"><div class="conf-fill" style="width:{pct}%; background:{c};"></div></div>
          <div class="conf-pct">{pct:.1f}%</div>
        </div>"""
    html += '</div>'
    return html

def render_label_chips(active_label=""):
    active = active_label.lower()
    chips = ""
    for lbl in LABELS:
        cls = "label-chip active" if lbl.lower() == active else "label-chip"
        chips += f'<div class="{cls}">{lbl.capitalize()}</div>'
    return f'<div class="label-grid">{chips}</div>'

def render_prediction(audio_bytes, model_ready):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    try:
        audio_np = preprocess_bytes(audio_bytes)
        if model_ready:
            result   = predict_from_bytes(audio_bytes)
            is_demo  = False
        else:
            result   = predict_demo(audio_np)
            is_demo  = True

        label  = result["label_capitalized"]
        conf   = result["confidence_pct"]
        probs  = result["probabilities"]
        top_k  = result["top_k"]

        # Prediction Card
        demo_note = "⚠️ DEMO MODE" if is_demo else "HASIL PREDIKSI"
        st.markdown(f"""
        <div class="pred-card">
          <div class="pred-label">{demo_note}</div>
          <div class="pred-name">{label}</div>
          <div class="pred-conf">Confidence Score: <strong>{conf:.1f}%</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence bars
        st.markdown(render_confidence_bars(top_k), unsafe_allow_html=True)

        # Plotly Gauge Chart
        try:
            import plotly.graph_objects as go
            fig_g = go.Figure(go.Indicator(
                mode  = "gauge+number",
                value = conf,
                number= {"suffix":"%","font":{"size":24,"color":"#38BDF8"}},
                gauge = {
                    "axis"     : {"range":[0,100],"tickcolor":"#4B5563","tickfont":{"color":"#9CA3AF"}},
                    "bar"      : {"color":"#38BDF8"},
                    "bgcolor"  : "#111827",
                    "borderwidth": 0,
                    "steps"    : [
                        {"range":[0,40], "color":"rgba(244,63,94,.1)"},
                        {"range":[40,70],"color":"rgba(245,158,11,.1)"},
                        {"range":[70,100],"color":"rgba(16,185,129,.1)"},
                    ],
                    "threshold": {"line":{"color":"#10B981","width":3},"thickness":0.8,"value":conf},
                },
            ))
            fig_g.update_layout(height=200, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="rgba(0,0,0,0)", font_color="#9CA3AF")
            st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})
        except ImportError:
            pass

        # MFCC Plots
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="sec-eyebrow">Visualisasi MFCC</div>', unsafe_allow_html=True)
        fig_m = plot_mfcc(audio_np, title=f"MFCC — {label} ({conf:.1f}%)")
        fig_m.patch.set_alpha(0.0) # Transparent bg
        st.pyplot(fig_m, use_container_width=True)
        plt.close(fig_m)

        fig_c = plot_confidence(LABELS, probs)
        fig_c.patch.set_alpha(0.0)
        st.pyplot(fig_c, use_container_width=True)
        plt.close(fig_c)

        # TTS Output
        st.markdown("<hr>", unsafe_allow_html=True)
        if TTS_OK:
            tts_text = f"Nama yang terdeteksi adalah {label}"
            key_base = f"tts_{label}_{conf:.0f}"
            if st.button("🔊 Putar Hasil Prediksi", use_container_width=True, key=key_base):
                with st.spinner("Mensintesis audio..."):
                    try:
                        audio_out = generate_speech_bytes(tts_text, voice="id-ID-GadisNeural", rate="+0%")
                        st.audio(audio_out, format="audio/mp3")
                        st.download_button(
                            "⬇️ Download MP3", data=audio_out, file_name=f"hasil_{label.lower()}.mp3",
                            mime="audio/mpeg", use_container_width=True, key=f"dl_{key_base}"
                        )
                    except Exception as e:
                        st.error(f"TTS Error: {e}")
        else:
            st.info("Modul TTS tidak tersedia.")

        st.session_state["asr_result"] = label.lower()
        st.session_state["asr_text"]   = f"Nama yang terdeteksi adalah {label}."

    except Exception as e:
        st.error(f"❌ Error saat memproses audio: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
defaults = {"page":"home","asr_result":"","asr_text":"","tts_voice":"id-ID-GadisNeural","tts_speed":"+0%","tts_volume":"+0%"}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TOP NAV
# ══════════════════════════════════════════════════════════════════════════════
def render_nav():
    p = st.session_state.page
    def ac(x): return "nav-pill active" if p == x else "nav-pill"

    st.markdown(f"""
    <div class="topnav">
      <div class="logo-wrap">
        <div class="logo-icon">🎙️</div>
        <span class="logo-name">SuaraKita</span>
      </div>
      <div class="nav-pills">
        <span class="{ac('home')}">Beranda</span>
        <span class="{ac('asr')}">ASR</span>
        <span class="{ac('tts')}">TTS</span>
        <span class="{ac('about')}">Pipeline</span>
      </div>
      <div class="nav-status">
        <div class="status-dot"></div> SYSTEM ONLINE
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Hidden routing
    c1, c2, c3, c4, _ = st.columns([1, 1, 1, 1, 4])
    with c1:
        if st.button("🏠 Beranda", key="n_home"): st.session_state.page = "home"; st.rerun()
    with c2:
        if st.button("🎤 ASR", key="n_asr"): st.session_state.page = "asr"; st.rerun()
    with c3:
        if st.button("🔊 TTS", key="n_tts"): st.session_state.page = "tts"; st.rerun()
    with c4:
        if st.button("ℹ️ Pipeline", key="n_about"): st.session_state.page = "about"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="hero">
      <div class="hero-badge"><span style="color:var(--sky);">●</span> ID AI VOICE PLATFORM</div>
      <h1 class="hero-h1">Transform Voice Into<br><span class="hero-h1-grad">Prediction</span></h1>
      <p class="hero-sub">Platform ASR dan Neural TTS Bahasa Indonesia berbasis Deep Learning dan CNN untuk pengenalan suara dan sintesis suara natural.</p>
    </div>
    """, unsafe_allow_html=True)

    _, c1, c2, _ = st.columns([2, 1, 1, 2])
    with c1:
        if st.button("🎤 Start Recognition", use_container_width=True): st.session_state.page = "asr"; st.rerun()
    with c2:
        if st.button("🔊 Generate Voice", use_container_width=True): st.session_state.page = "tts"; st.rerun()

    st.markdown(render_waveform(), unsafe_allow_html=True)
    st.markdown('<div class="down-arrow">↓</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-strip">
      <div class="stat-cell"><div class="stat-val">12+</div><div class="stat-lbl">Kelas Nama</div></div>
      <div class="stat-cell"><div class="stat-val">500+</div><div class="stat-lbl">Audio Dataset</div></div>
      <div class="stat-cell"><div class="stat-val">CNN</div><div class="stat-lbl">Architecture</div></div>
      <div class="stat-cell"><div class="stat-val">13</div><div class="stat-lbl">MFCC Features</div></div>
    </div>
    """, unsafe_allow_html=True)

    cc1, cc2 = st.columns(2, gap="medium")
    with cc1:
        st.markdown("""
        <div class="gc">
          <div style="width:50px;height:50px;border-radius:12px;background:rgba(139,92,246,.1);color:#8B5CF6;
                display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:16px;border:1px solid rgba(139,92,246,.2);">🎤</div>
          <h3 style="font-size:1.25rem;font-weight:700;margin-bottom:10px;">Automatic Speech Recognition</h3>
          <p style="color:var(--text-muted);font-size:0.9rem;line-height:1.6;">Rekam dari mikrofon atau upload WAV. Ekstraksi 13 MFCC coefficients, klasifikasi CNN 1D, confidence score real-time.</p>
          <div class="tech-wrap">
            <span class="tech-tag-blue">MFCC</span><span class="tech-tag-blue">CNN 1D</span><span class="tech-tag-blue">Real-time</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with cc2:
        st.markdown("""
        <div class="gc">
          <div style="width:50px;height:50px;border-radius:12px;background:rgba(236,72,153,.1);color:#EC4899;
                display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin-bottom:16px;border:1px solid rgba(236,72,153,.2);">🔊</div>
          <h3 style="font-size:1.25rem;font-weight:700;margin-bottom:10px;">Neural Text-to-Speech</h3>
          <p style="color:var(--text-muted);font-size:0.9rem;line-height:1.6;">Konversi teks Bahasa Indonesia ke suara natural menggunakan Microsoft Edge TTS Neural Voice. Pilih suara, atur kecepatan, download MP3.</p>
          <div class="tech-wrap">
            <span class="tech-tag-purple">edge-tts</span><span class="tech-tag-purple">Neural Voice</span><span class="tech-tag-purple">MP3 Export</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="down-arrow">↓</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ASR (With intact tabs & backend)
# ══════════════════════════════════════════════════════════════════════════════
def page_asr():
    st.markdown("""
    <div>
      <div class="sec-title">Automatic Speech Recognition</div>
      <div class="sec-desc">Rekam dari mikrofon atau upload WAV — CNN 1D memprediksi nama dengan MFCC 13 koefisien.</div>
    </div>
    """, unsafe_allow_html=True)

    if not ASR_OK:
        st.error(f"❌ Modul ASR tidak tersedia: {ASR_ERR}")
        return

    model_ready = is_model_available()
    if not model_ready:
        st.markdown("""
        <div class="demo-warn">
          <span>⚠️</span>
          <div><strong>Mode Demo Aktif</strong> — File <code>model_asr.h5</code> belum ditemukan.</div>
        </div>
        """, unsafe_allow_html=True)

    tab_mic, tab_up, tab_info = st.tabs(["🎙️ Mikrofon", "📂 Upload Audio", "📋 Panduan Dataset"])

    with tab_mic:
        m_col, s_col = st.columns([1.2, 1], gap="large")
        with m_col:
            st.markdown("<div class='gc-accent'>", unsafe_allow_html=True)
            st.markdown("<strong style='color:var(--text);'>Rekam Suara (1-2 Detik)</strong><br><br>", unsafe_allow_html=True)
            audio_rec = st.audio_input("Klik ikon mic untuk merekam")
            if audio_rec:
                ab = audio_rec.read()
                st.audio(ab, format="audio/wav")
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                if st.button("🚀 Analisis & Prediksi", use_container_width=True):
                    with st.spinner("Memproses..."):
                        render_prediction(ab, model_ready)
            st.markdown("</div>", unsafe_allow_html=True)
        with s_col:
            active = st.session_state.get("asr_result", "")
            st.markdown('<div class="sec-eyebrow">Kelas Tersedia</div>', unsafe_allow_html=True)
            st.markdown(render_label_chips(active), unsafe_allow_html=True)

    with tab_up:
        u_col, us_col = st.columns([1.2, 1], gap="large")
        with u_col:
            st.markdown("<div class='gc-accent'>", unsafe_allow_html=True)
            st.markdown("<strong style='color:var(--text);'>Upload File Audio</strong><br><br>", unsafe_allow_html=True)
            uploaded = st.file_uploader("Pilih WAV / MP3 / OGG", type=["wav","mp3","ogg"])
            if uploaded:
                ab = uploaded.read()
                st.audio(ab, format="audio/wav")
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                if st.button("🚀 Analisis Upload", use_container_width=True):
                    with st.spinner("Memproses..."):
                        render_prediction(ab, model_ready)
            st.markdown("</div>", unsafe_allow_html=True)
        with us_col:
            active2 = st.session_state.get("asr_result", "")
            st.markdown('<div class="sec-eyebrow">Kelas Tersedia</div>', unsafe_allow_html=True)
            st.markdown(render_label_chips(active2), unsafe_allow_html=True)

    with tab_info:
        i1, i2 = st.columns(2, gap="large")
        with i1:
            st.markdown('<div class="sec-eyebrow">Struktur Dataset</div>', unsafe_allow_html=True)
            st.code("dataset/\n├── yesus/\n├── simon/\n└── [10 kelas lainnya]", language="text")
        with i2:
            st.markdown('<div class="sec-eyebrow">Arsitektur Model</div>', unsafe_allow_html=True)
            st.code("Input: (32, 13)\nConv1D (32) -> MaxPool\nConv1D (64) -> MaxPool\nDense(128) -> Dropout\nDense(12, Softmax)", language="text")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TTS
# ══════════════════════════════════════════════════════════════════════════════
def page_tts():
    st.markdown("""
    <div>
      <div class="sec-title">Neural Text-to-Speech</div>
      <div class="sec-desc">Teks Bahasa Indonesia → suara neural natural. Pilih voice, atur kecepatan & volume.</div>
    </div>
    """, unsafe_allow_html=True)

    if not TTS_OK:
        st.error("❌ Modul TTS tidak tersedia.")
        return

    t_col, s_col = st.columns([1.5, 1], gap="large")

    with t_col:
        st.markdown("<div class='gc'>", unsafe_allow_html=True)
        asr_text = st.session_state.get("asr_text", "")
        if asr_text:
            st.success("Teks dari hasil ASR otomatis terisi.")
        
        default_text = asr_text if asr_text else "Halo, sistem mendeteksi anomali pada lingkungan. Semua unit bersiap."
        text_in = st.text_area("Masukkan Teks:", value=default_text, height=150)
        
        if st.button("✨ Generate Neural Voice", use_container_width=True):
            if not text_in.strip():
                st.warning("Teks kosong!")
            else:
                with st.spinner("Rendering..."):
                    try:
                        vid = st.session_state.get("tts_voice", "id-ID-GadisNeural")
                        spd = st.session_state.get("tts_speed", "+0%")
                        vol = st.session_state.get("tts_volume", "+0%")
                        ab  = generate_speech_bytes(text_in, voice=vid, rate=spd, volume=vol)

                        st.success("Audio Siap!")
                        st.audio(ab, format="audio/mp3")
                        st.download_button("⬇️ Download MP3", data=ab, file_name="suarakita.mp3", mime="audio/mpeg", use_container_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with s_col:
        st.markdown("<div class='gc'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-eyebrow">Voice Settings</div>', unsafe_allow_html=True)

        vnames = list_voices()
        sel_v  = st.selectbox("Model Voice", vnames, index=0)
        st.session_state["tts_voice"] = get_voice_id(sel_v)

        spds   = list_speeds()
        sel_s  = st.selectbox("Speed (Rate)", spds, index=1)
        st.session_state["tts_speed"] = get_speed_value(sel_s)

        vols   = list_volumes()
        sel_vol= st.selectbox("Volume", vols, index=1)
        st.session_state["tts_volume"] = get_volume_value(sel_vol)

        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT / PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def page_about():
    st.markdown("""
    <div>
      <div class="sec-title">System Pipeline & Architecture</div>
      <div class="sec-desc">Alur kerja sistem pengenalan suara dan sintesis suara.</div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline diagram
    st.markdown('<div class="gc" style="margin-bottom:2rem;">', unsafe_allow_html=True)
    pipe_steps = [
        ("🎙️","Audio Input","WAV"),
        ("⚙️","Preprocess","Norm"),
        ("📈","MFCC","13 Coef"),
        ("🧠","CNN 1D","Inferensi"),
        ("📄","Prediction","Output"),
        ("🔊","Edge TTS","Audio")
    ]
    html = '<div class="pipeline">'
    for i, (icon, title, sub) in enumerate(pipe_steps):
        html += f"""
        <div class="pipe-node">
          <div class="pipe-icon">{icon}</div>
          <div class="pipe-title">{title}</div>
          <div class="pipe-sub">{sub}</div>
        </div>"""
        if i < len(pipe_steps)-1: html += '<div class="pipe-connector"></div>'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div class="gc">
          <div class="sec-eyebrow">Teknologi ASR</div>
          <div class="tech-wrap">
            <span class="tech-tag-blue">Librosa</span><span class="tech-tag-blue">TensorFlow / Keras</span>
            <span class="tech-tag-blue">NumPy</span><span class="tech-tag-blue">Matplotlib</span>
          </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="gc">
          <div class="sec-eyebrow">Teknologi TTS</div>
          <div class="tech-wrap">
            <span class="tech-tag-purple">edge-tts</span><span class="tech-tag-purple">asyncio</span>
            <span class="tech-tag-purple">Neural Voice</span><span class="tech-tag-purple">MP3 Format</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="wrap">', unsafe_allow_html=True)
render_nav()

pg = st.session_state.page
if   pg == "home":  page_home()
elif pg == "asr":   page_asr()
elif pg == "tts":   page_tts()
elif pg == "about": page_about()
else:               page_home()

st.markdown('</div>', unsafe_allow_html=True)