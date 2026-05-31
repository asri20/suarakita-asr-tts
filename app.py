"""
app.py - SuaraKita ASR + TTS Bahasa Indonesia
Premium AI Interface Redesign — ElevenLabs / OpenAI Voice Mode Aesthetic
"""

import os
import sys
import time
import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SuaraKita — AI Voice Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Premium dark AI aesthetic
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ─── Fonts ─────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Cal+Sans&family=Bricolage+Grotesque:opsz,wght@12..96,200;12..96,300;12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ─── Design Tokens ─────────────────────────────────────────────────────── */
:root {
  --bg:           #050816;
  --bg-1:         #080d20;
  --bg-2:         #0d1530;
  --surface:      rgba(255,255,255,0.04);
  --surface-2:    rgba(255,255,255,0.07);
  --surface-3:    rgba(255,255,255,0.11);
  --border:       rgba(255,255,255,0.08);
  --border-2:     rgba(255,255,255,0.14);

  --blue:         #3B82F6;
  --cyan:         #06B6D4;
  --purple:       #8B5CF6;
  --violet:       #7C3AED;
  --pink:         #EC4899;
  --green:        #10B981;
  --amber:        #F59E0B;

  --grad-primary: linear-gradient(135deg, #3B82F6 0%, #06B6D4 50%, #8B5CF6 100%);
  --grad-glow:    linear-gradient(135deg, rgba(59,130,246,0.3), rgba(6,182,212,0.3), rgba(139,92,246,0.3));
  --grad-card:    linear-gradient(145deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.02) 100%);

  --text:         #F8FAFC;
  --text-2:       #CBD5E1;
  --text-3:       #94A3B8;
  --text-4:       #64748B;

  --r-sm:         12px;
  --r-md:         18px;
  --r-lg:         24px;
  --r-xl:         32px;

  --shadow-blue:  0 0 40px rgba(59,130,246,0.15);
  --shadow-cyan:  0 0 40px rgba(6,182,212,0.15);
  --shadow-glow:  0 0 80px rgba(99,102,241,0.2);
  --shadow-card:  0 8px 32px rgba(0,0,0,0.4), 0 1px 0 rgba(255,255,255,0.05) inset;
}

/* ─── Base Reset ────────────────────────────────────────────────────────── */
html, body, .stApp {
  background: var(--bg) !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased;
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ─── Animated Grain Texture ────────────────────────────────────────────── */
body::before {
  content: '';
  position: fixed; inset: 0; z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  opacity: 0.4;
}

/* ─── Ambient glow orbs ─────────────────────────────────────────────────── */
body::after {
  content: '';
  position: fixed;
  top: -40%; left: -10%;
  width: 70vw; height: 70vw;
  background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ─── Hide streamlit sidebar completely ─────────────────────────────────── */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ─── Main layout wrapper ───────────────────────────────────────────────── */
.main-wrap {
  position: relative; z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px 80px 32px;
}

/* ─── Top Navigation ────────────────────────────────────────────────────── */
.topnav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0 20px 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 56px;
  position: sticky;
  top: 0;
  background: rgba(5,8,22,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 100;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  text-decoration: none;
}
.nav-logo-icon {
  width: 36px; height: 36px;
  background: var(--grad-primary);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  box-shadow: 0 0 20px rgba(59,130,246,0.4);
}
.nav-logo-text {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-links {
  display: flex; gap: 4px;
}
.nav-link {
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-3);
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  white-space: nowrap;
}
.nav-link:hover {
  color: var(--text);
  background: var(--surface-2);
}
.nav-link.active {
  color: var(--text);
  background: var(--surface-3);
  border-color: var(--border-2);
}
.nav-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  background: rgba(59,130,246,0.15);
  border: 1px solid rgba(59,130,246,0.3);
  color: #60A5FA;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* ─── Hero ──────────────────────────────────────────────────────────────── */
.hero-wrap {
  text-align: center;
  padding: 80px 20px 100px;
  position: relative;
  overflow: hidden;
}
.hero-orb-1 {
  position: absolute; top: -20%; left: 10%;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
  pointer-events: none;
  animation: pulse-orb 6s ease-in-out infinite;
}
.hero-orb-2 {
  position: absolute; top: -10%; right: 5%;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%);
  pointer-events: none;
  animation: pulse-orb 8s ease-in-out infinite reverse;
}
@keyframes pulse-orb {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.15); opacity: 1; }
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(59,130,246,0.1);
  border: 1px solid rgba(59,130,246,0.25);
  color: #60A5FA;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 28px;
}
.hero-eyebrow-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #60A5FA;
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.hero-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(2.8rem, 6vw, 5rem);
  font-weight: 800;
  line-height: 1.05;
  margin: 0 0 20px 0;
  letter-spacing: -0.03em;
}
.hero-title-plain { color: var(--text); }
.hero-title-grad {
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 1.15rem;
  color: var(--text-3);
  max-width: 600px;
  margin: 0 auto 44px;
  line-height: 1.65;
  font-weight: 400;
}
.hero-cta {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 26px;
  border-radius: 12px;
  background: var(--grad-primary);
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  border: none;
  transition: all 0.25s;
  box-shadow: 0 4px 24px rgba(59,130,246,0.35);
  font-family: 'Bricolage Grotesque', sans-serif;
  text-decoration: none;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(59,130,246,0.5);
}
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 13px 26px;
  border-radius: 12px;
  background: var(--surface-2);
  border: 1px solid var(--border-2);
  color: var(--text-2);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.25s;
  font-family: 'Bricolage Grotesque', sans-serif;
  text-decoration: none;
}
.btn-secondary:hover {
  background: var(--surface-3);
  border-color: rgba(255,255,255,0.2);
  color: var(--text);
  transform: translateY(-2px);
}

/* ─── Waveform Animation ────────────────────────────────────────────────── */
.waveform-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  height: 64px;
  margin: 44px auto 0;
  max-width: 360px;
}
.wave-bar {
  width: 3px;
  border-radius: 3px;
  background: var(--grad-primary);
  animation: wave 1.4s ease-in-out infinite;
  opacity: 0.7;
}
@keyframes wave {
  0%, 100% { height: 8px; opacity: 0.3; }
  50%       { height: 48px; opacity: 0.9; }
}

/* ─── Stats strip ───────────────────────────────────────────────────────── */
.stats-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border);
  border-radius: var(--r-lg);
  overflow: hidden;
  margin-bottom: 72px;
}
.stat-item {
  background: var(--surface);
  padding: 28px 24px;
  text-align: center;
  backdrop-filter: blur(10px);
}
.stat-value {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 2.2rem;
  font-weight: 800;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 6px;
}
.stat-label {
  font-size: 0.82rem;
  color: var(--text-4);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

/* ─── Section heading ───────────────────────────────────────────────────── */
.section-label {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--cyan);
  margin-bottom: 10px;
}
.section-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 800;
  color: var(--text);
  margin: 0 0 12px 0;
  letter-spacing: -0.02em;
}
.section-desc {
  font-size: 1rem;
  color: var(--text-3);
  margin: 0 0 40px 0;
  line-height: 1.6;
}

/* ─── Glass Cards ───────────────────────────────────────────────────────── */
.glass-card {
  background: var(--grad-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 28px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: var(--shadow-card);
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.glass-card:hover {
  border-color: var(--border-2);
  transform: translateY(-3px);
  box-shadow: var(--shadow-card), 0 0 40px rgba(59,130,246,0.08);
}
.glass-card-accent {
  background: var(--grad-card);
  border: 1px solid rgba(59,130,246,0.25);
  border-radius: var(--r-lg);
  padding: 28px;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow-card), inset 0 0 60px rgba(59,130,246,0.03);
}

/* ─── Feature cards home ────────────────────────────────────────────────── */
.feat-icon {
  width: 52px; height: 52px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 18px;
}
.feat-icon-blue  { background: rgba(59,130,246,0.15);  border: 1px solid rgba(59,130,246,0.3); }
.feat-icon-cyan  { background: rgba(6,182,212,0.15);   border: 1px solid rgba(6,182,212,0.3); }
.feat-icon-purple{ background: rgba(139,92,246,0.15);  border: 1px solid rgba(139,92,246,0.3); }
.feat-icon-green { background: rgba(16,185,129,0.15);  border: 1px solid rgba(16,185,129,0.3); }
.feat-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 8px 0;
}
.feat-desc {
  font-size: 0.9rem;
  color: var(--text-3);
  line-height: 1.6;
}
.feat-tags {
  display: flex; flex-wrap: wrap; gap: 6px; margin-top: 16px;
}
.feat-tag {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--surface-3);
  color: var(--text-3);
  border: 1px solid var(--border);
}

/* ─── Flow diagram home ─────────────────────────────────────────────────── */
.flow-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
  padding: 36px;
}
.flow-node {
  text-align: center;
  padding: 18px 22px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--r-md);
  min-width: 120px;
  transition: border-color 0.2s;
}
.flow-node:hover { border-color: var(--border-2); }
.flow-node-icon { font-size: 1.6rem; margin-bottom: 6px; }
.flow-node-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-2);
}
.flow-node-sub {
  font-size: 0.75rem;
  color: var(--text-4);
  margin-top: 3px;
}
.flow-arrow {
  font-size: 1.2rem;
  color: var(--text-4);
  padding: 0 8px;
  flex-shrink: 0;
}

/* ─── Label chips home ──────────────────────────────────────────────────── */
.label-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}
.label-chip {
  padding: 10px 14px;
  border-radius: 10px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-2);
  text-align: center;
  transition: all 0.2s;
  cursor: default;
}
.label-chip:hover {
  background: var(--surface-3);
  border-color: rgba(59,130,246,0.4);
  color: #60A5FA;
}

/* ─── ASR page layout ───────────────────────────────────────────────────── */
.page-header {
  padding: 40px 0 44px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 44px;
}
.page-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 800;
  color: var(--text);
  margin: 0 0 10px 0;
  letter-spacing: -0.025em;
}
.page-sub {
  font-size: 1rem;
  color: var(--text-3);
  max-width: 560px;
  line-height: 1.6;
}

/* ─── Microphone button ─────────────────────────────────────────────────── */
.mic-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 24px;
}
.mic-ring-outer {
  position: relative;
  width: 160px; height: 160px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 24px;
}
.mic-ring-outer::before {
  content: '';
  position: absolute; inset: -12px;
  border-radius: 50%;
  border: 1px solid rgba(59,130,246,0.2);
  animation: ping 2.5s ease-out infinite;
}
.mic-ring-outer::after {
  content: '';
  position: absolute; inset: -24px;
  border-radius: 50%;
  border: 1px solid rgba(59,130,246,0.1);
  animation: ping 2.5s ease-out infinite 0.5s;
}
@keyframes ping {
  0%   { transform: scale(0.95); opacity: 0.6; }
  100% { transform: scale(1.25); opacity: 0; }
}
.mic-btn {
  width: 160px; height: 160px;
  border-radius: 50%;
  background: var(--grad-primary);
  border: none;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 3rem;
  box-shadow: 0 0 60px rgba(59,130,246,0.4), 0 4px 32px rgba(0,0,0,0.5);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative; z-index: 1;
}
.mic-btn:hover {
  transform: scale(1.06);
  box-shadow: 0 0 80px rgba(59,130,246,0.6), 0 8px 48px rgba(0,0,0,0.5);
}
.mic-label {
  font-size: 0.95rem;
  color: var(--text-3);
  text-align: center;
}

/* ─── Demo notice ───────────────────────────────────────────────────────── */
.demo-notice {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: rgba(245,158,11,0.08);
  border: 1px solid rgba(245,158,11,0.25);
  border-radius: var(--r-md);
  padding: 14px 18px;
  font-size: 0.875rem;
  color: #FCD34D;
  margin-bottom: 28px;
  line-height: 1.5;
}

/* ─── Prediction result card ────────────────────────────────────────────── */
.pred-card {
  background: linear-gradient(145deg, rgba(16,185,129,0.08), rgba(59,130,246,0.08));
  border: 1px solid rgba(16,185,129,0.25);
  border-radius: var(--r-xl);
  padding: 40px 32px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.pred-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(16,185,129,0.6), transparent);
}
.pred-eyebrow {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--text-4);
  margin-bottom: 10px;
}
.pred-name {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #34D399, #60A5FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
  text-transform: capitalize;
  margin: 0 0 10px 0;
}
.pred-conf {
  font-size: 1rem;
  color: var(--text-3);
}
.pred-conf strong { color: #34D399; }

/* ─── Confidence bar ────────────────────────────────────────────────────── */
.conf-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}
.conf-rank {
  font-size: 0.8rem;
  color: var(--text-4);
  width: 20px;
  text-align: right;
  flex-shrink: 0;
}
.conf-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-2);
  width: 120px;
  flex-shrink: 0;
  text-transform: capitalize;
}
.conf-track {
  flex: 1;
  height: 6px;
  background: var(--surface-3);
  border-radius: 999px;
  overflow: hidden;
}
.conf-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.conf-pct {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-2);
  width: 50px;
  text-align: right;
  flex-shrink: 0;
  font-family: 'JetBrains Mono', monospace;
}

/* ─── Upload zone ───────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  background: var(--surface) !important;
  border: 1.5px dashed var(--border-2) !important;
  border-radius: var(--r-lg) !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: rgba(59,130,246,0.5) !important;
}
[data-testid="stFileUploader"] * { color: var(--text-3) !important; }
[data-testid="stFileUploaderDropzone"] {
  background: transparent !important;
  padding: 32px !important;
}

/* ─── Audio input ───────────────────────────────────────────────────────── */
[data-testid="stAudioInput"] {
  background: var(--surface) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--r-lg) !important;
  padding: 12px !important;
}

/* ─── Audio player ──────────────────────────────────────────────────────── */
audio {
  width: 100%;
  border-radius: 12px;
  background: var(--surface-2);
}

/* ─── Streamlit buttons → premium override ──────────────────────────────── */
.stButton > button {
  background: var(--grad-primary) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  padding: 12px 24px !important;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
  box-shadow: 0 4px 20px rgba(59,130,246,0.25) !important;
  letter-spacing: 0.01em !important;
  width: 100%;
}
.stButton > button:hover {
  opacity: 0.9 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(59,130,246,0.4) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
}

/* Secondary button variant */
.btn-ghost .stButton > button {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-2) !important;
  color: var(--text-2) !important;
  box-shadow: none !important;
}
.btn-ghost .stButton > button:hover {
  background: var(--surface-3) !important;
  box-shadow: none !important;
}

/* ─── Text inputs ───────────────────────────────────────────────────────── */
.stTextArea textarea {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--r-md) !important;
  color: var(--text) !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-size: 0.95rem !important;
  line-height: 1.6 !important;
  resize: vertical;
}
.stTextArea textarea:focus {
  border-color: rgba(59,130,246,0.6) !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
.stTextArea label { color: var(--text-3) !important; font-size: 0.85rem !important; }

/* ─── Selectbox ─────────────────────────────────────────────────────────── */
.stSelectbox > div > div {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
}
.stSelectbox label { color: var(--text-3) !important; font-size: 0.85rem !important; }

/* ─── Slider ────────────────────────────────────────────────────────────── */
.stSlider > div { color: var(--text-3) !important; }

/* ─── Tabs ──────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 14px !important;
  padding: 5px !important;
  border: 1px solid var(--border) !important;
  gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important;
  color: var(--text-4) !important;
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 8px 18px !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(59,130,246,0.2) !important;
  color: #60A5FA !important;
  border: 1px solid rgba(59,130,246,0.3) !important;
}
.stTabs [data-testid="stTabContent"] {
  padding: 24px 0 0 0 !important;
}

/* ─── Divider ───────────────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 28px 0 !important; }

/* ─── Caption / help text ───────────────────────────────────────────────── */
.stCaption, .stMarkdown small { color: var(--text-4) !important; }

/* ─── Info / warning / error boxes ─────────────────────────────────────── */
.stAlert {
  border-radius: var(--r-md) !important;
  border: 1px solid var(--border) !important;
  background: var(--surface) !important;
}

/* ─── TTS voice settings card ───────────────────────────────────────────── */
.settings-card {
  background: var(--grad-card);
  border: 1px solid var(--border);
  border-radius: var(--r-lg);
  padding: 24px;
  backdrop-filter: blur(16px);
  margin-bottom: 16px;
}
.settings-label {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-4);
  margin-bottom: 12px;
}
.voice-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 8px;
}

/* ─── About page cards ──────────────────────────────────────────────────── */
.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  margin-top: 16px;
}
.tech-pill {
  padding: 8px 14px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-3);
  text-align: center;
  transition: all 0.2s;
}
.tech-pill:hover {
  border-color: rgba(59,130,246,0.4);
  color: #60A5FA;
  background: rgba(59,130,246,0.08);
}

.spec-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.spec-item {
  background: var(--surface-2);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  border: 1px solid var(--border);
}
.spec-val {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.6rem;
  font-weight: 800;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  margin-bottom: 4px;
}
.spec-lbl {
  font-size: 0.75rem;
  color: var(--text-4);
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

/* ─── Sidebar label fix ─────────────────────────────────────────────────── */
.stRadio label { color: var(--text-2) !important; }
.stRadio > div { gap: 4px !important; }

/* ─── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-2); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ─── Code blocks ───────────────────────────────────────────────────────── */
.stCode, code {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  font-family: 'JetBrains Mono', monospace !important;
  color: var(--text-2) !important;
  font-size: 0.82rem !important;
}

/* ─── Mobile responsive ─────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .main-wrap { padding: 0 16px 60px; }
  .stats-strip { grid-template-columns: repeat(2, 1fr); }
  .hero-title { font-size: 2.2rem; }
  .topnav { flex-wrap: wrap; gap: 12px; }
  .flow-wrap { gap: 8px; }
  .nav-links { display: none; }
  .spec-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
try:
    from asr import (
        LABELS, SAMPLE_RATE,
        preprocess_bytes, preprocess_audio,
        load_audio_from_bytes,
        extract_mfcc, plot_mfcc, plot_confidence,
        predict_from_bytes, predict_demo, is_model_available,
    )
    ASR_AVAILABLE = True
    ASR_ERROR = ""
except ImportError as e:
    ASR_AVAILABLE = False
    ASR_ERROR = str(e)
    LABELS = ["yesus","simon","andreas","yakobus","yohanes","filipus",
              "bartomeleus","tomas","matius","tadeus","yudas","maria"]

try:
    from tts import (
        generate_speech_bytes, list_voices, list_speeds, list_volumes,
        get_voice_id, get_speed_value, get_volume_value,
    )
    TTS_AVAILABLE = True
    TTS_ERROR = ""
except ImportError as e:
    TTS_AVAILABLE = False
    TTS_ERROR = str(e)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE — page routing
# ══════════════════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "home"

# ══════════════════════════════════════════════════════════════════════════════
# TOP NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def topnav():
    p = st.session_state.page
    home_cls = "nav-link active" if p == "home"  else "nav-link"
    asr_cls  = "nav-link active" if p == "asr"   else "nav-link"
    tts_cls  = "nav-link active" if p == "tts"   else "nav-link"
    abt_cls  = "nav-link active" if p == "about" else "nav-link"

    st.markdown(f"""
    <div class="topnav">
      <div class="nav-logo">
        <div class="nav-logo-icon">🎙️</div>
        <span class="nav-logo-text">SuaraKita</span>
      </div>
      <div class="nav-links">
        <span class="{home_cls}" id="nav-home">Beranda</span>
        <span class="{asr_cls}" id="nav-asr">Speech Recognition</span>
        <span class="{tts_cls}" id="nav-tts">Text-to-Speech</span>
        <span class="{abt_cls}" id="nav-about">Tentang</span>
      </div>
      <div>
        <span class="nav-badge">🇮🇩 Bahasa Indonesia</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Row of actual buttons hidden as nav (Streamlit limitation)
    c1, c2, c3, c4, _ = st.columns([1, 1.4, 1.2, 1, 4])
    with c1:
        if st.button("🏠 Beranda", use_container_width=True, key="nav_home"):
            st.session_state.page = "home"; st.rerun()
    with c2:
        if st.button("🎤 ASR", use_container_width=True, key="nav_asr"):
            st.session_state.page = "asr"; st.rerun()
    with c3:
        if st.button("🔊 TTS", use_container_width=True, key="nav_tts"):
            st.session_state.page = "tts"; st.rerun()
    with c4:
        if st.button("ℹ️ Tentang", use_container_width=True, key="nav_about"):
            st.session_state.page = "about"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HELPER: render prediction results
# ══════════════════════════════════════════════════════════════════════════════
def render_prediction(audio_bytes, model_ready):
    try:
        audio_np = preprocess_bytes(audio_bytes)
        if model_ready:
            result  = predict_from_bytes(audio_bytes)
            is_demo = False
        else:
            result  = predict_demo(audio_np)
            is_demo = True

        label = result["label_capitalized"]
        conf  = result["confidence_pct"]
        probs = result["probabilities"]
        top_k = result["top_k"]

        # ── Prediction card ──────────────────────────────────────────────
        st.markdown(f"""
        <div class="pred-card">
          <div class="pred-eyebrow">
            {"⚠️ Demo Mode — " if is_demo else "✦ Prediksi Nama"}
          </div>
          <div class="pred-name">{label}</div>
          <div class="pred-conf">
            Confidence: <strong>{conf:.1f}%</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Top-K confidence bars ────────────────────────────────────────
        st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-label">Confidence Scores</div>
        """, unsafe_allow_html=True)

        bar_colors = ["#10B981", "#3B82F6", "#8B5CF6", "#06B6D4", "#F59E0B"]
        for i, (lbl, p) in enumerate(top_k):
            pct   = p * 100
            color = bar_colors[i] if i < len(bar_colors) else "#64748B"
            rank  = ["🥇","🥈","🥉","4","5"][i] if i < 5 else str(i+1)
            st.markdown(f"""
            <div class="conf-row">
              <div class="conf-rank">{rank}</div>
              <div class="conf-label">{lbl.capitalize()}</div>
              <div class="conf-track">
                <div class="conf-fill" style="width:{pct:.1f}%; background:{color};"></div>
              </div>
              <div class="conf-pct">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── MFCC Visualization ───────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-label">Visualisasi MFCC</div>', unsafe_allow_html=True)
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig_mfcc = plot_mfcc(audio_np, title=f"MFCC — {label} ({conf:.1f}%)")
        st.pyplot(fig_mfcc, use_container_width=True)
        plt.close(fig_mfcc)

        fig_conf = plot_confidence(LABELS, probs)
        st.pyplot(fig_conf, use_container_width=True)
        plt.close(fig_conf)

        # ── TTS Integration ──────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-label">Lanjutkan ke TTS</div>', unsafe_allow_html=True)
        if TTS_AVAILABLE:
            tts_text = f"Nama yang terdeteksi adalah {label}"
            if st.button("🔊 Bacakan Hasil Prediksi", use_container_width=True,
                         key=f"tts_btn_{label}_{conf:.0f}"):
                with st.spinner("Membuat audio..."):
                    try:
                        audio_out = generate_speech_bytes(
                            tts_text, voice="id-ID-GadisNeural", rate="+0%")
                        st.audio(audio_out, format="audio/mp3")
                        st.download_button(
                            "⬇️ Download MP3",
                            data=audio_out,
                            file_name=f"hasil_{label.lower()}.mp3",
                            mime="audio/mpeg",
                            key=f"dl_{label}_{conf:.0f}",
                            use_container_width=True,
                        )
                    except Exception as e:
                        st.error(f"TTS Error: {e}")
        else:
            st.info("Modul TTS tidak tersedia.")

        st.session_state["asr_result"] = label
        st.session_state["asr_text"]   = f"Nama yang terdeteksi adalah {label}"

    except Exception as e:
        st.error(f"❌ Error saat memproses: {e}")
        st.exception(e)

# ══════════════════════════════════════════════════════════════════════════════
# WAVEFORM BARS helper
# ══════════════════════════════════════════════════════════════════════════════
def waveform_bars(n=28):
    import random
    bars = ""
    delays = [round(i * 0.06, 2) for i in range(n)]
    for d in delays:
        bars += f'<div class="wave-bar" style="animation-delay:{d}s;"></div>'
    return f'<div class="waveform-container">{bars}</div>'

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    # Hero
    st.markdown(f"""
    <div class="hero-wrap">
      <div class="hero-orb-1"></div>
      <div class="hero-orb-2"></div>
      <div class="hero-eyebrow">
        <span class="hero-eyebrow-dot"></span>
        AI Voice Platform · Bahasa Indonesia
      </div>
      <h1 class="hero-title">
        <span class="hero-title-plain">Transform Voice Into</span><br>
        <span class="hero-title-grad">Intelligence</span>
      </h1>
      <p class="hero-sub">
        Platform ASR & TTS Bahasa Indonesia berbasis Deep Learning.
        Kenali nama dari suara dengan Neural Network CNN, dan ubah teks
        menjadi suara natural menggunakan Microsoft Neural TTS.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons
    c1, c2, c3 = st.columns([2,1,1,])
    with c2:
        if st.button("🎤 Speech Recognition", use_container_width=True, key="cta_asr"):
            st.session_state.page = "asr"; st.rerun()
    with c3:
        if st.button("🔊 Generate AI Voice", use_container_width=True, key="cta_tts"):
            st.session_state.page = "tts"; st.rerun()

    st.markdown(waveform_bars(32), unsafe_allow_html=True)

    st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

    # Stats strip
    asr_status = "🟢 Ready" if ASR_AVAILABLE else "🔴 Error"
    tts_status = "🟢 Ready" if TTS_AVAILABLE else "🔴 Error"
    model_st   = "🟢 Loaded" if (ASR_AVAILABLE and is_model_available()) else "🟡 Demo"

    st.markdown(f"""
    <div class="stats-strip">
      <div class="stat-item">
        <div class="stat-value">12</div>
        <div class="stat-label">Kelas Nama</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">500+</div>
        <div class="stat-label">Audio Dataset</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">CNN</div>
        <div class="stat-label">Arsitektur</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">13</div>
        <div class="stat-label">Koefisien MFCC</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col_a, col_b = st.columns(2, gap="medium")
    with col_a:
        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-blue">🎤</div>
          <div class="feat-title">Automatic Speech Recognition</div>
          <div class="feat-desc">
            Rekam langsung dari mikrofon atau upload file WAV. Sistem mengekstrak
            13 koefisien MFCC dan memprediksi nama menggunakan CNN 1D yang dilatih
            dengan dataset Bahasa Indonesia.
          </div>
          <div class="feat-tags">
            <span class="feat-tag">MFCC Features</span>
            <span class="feat-tag">CNN 1D Model</span>
            <span class="feat-tag">Real-time</span>
            <span class="feat-tag">Confidence Score</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-cyan">🔊</div>
          <div class="feat-title">Neural Text-to-Speech</div>
          <div class="feat-desc">
            Konversi teks Bahasa Indonesia menjadi suara berkualitas tinggi menggunakan
            Microsoft edge-tts Neural Voice. Pilih suara pria/wanita, atur kecepatan
            dan volume, lalu download MP3.
          </div>
          <div class="feat-tags">
            <span class="feat-tag">edge-tts</span>
            <span class="feat-tag">Neural Voice</span>
            <span class="feat-tag">MP3 Export</span>
            <span class="feat-tag">Multilingual</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)

    # Label grid
    st.markdown("""
    <div class="section-label">Kelas yang Dikenali</div>
    <div class="section-title">12 Nama Bahasa Indonesia</div>
    <div class="section-desc">Model dilatih untuk mengenali nama-nama berikut dari rekaman suara.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="label-grid">', unsafe_allow_html=True)
    for lbl in LABELS:
        st.markdown(f'<div class="label-chip">📌 {lbl.capitalize()}</div>',
                    unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

    # Pipeline diagram
    st.markdown("""
    <div class="section-label">Pipeline</div>
    <div class="section-title">Alur ASR → TTS</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card-accent">
      <div class="flow-wrap">
        <div class="flow-node">
          <div class="flow-node-icon">🎙️</div>
          <div class="flow-node-title">Audio Input</div>
          <div class="flow-node-sub">Mic / Upload</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-node">
          <div class="flow-node-icon">🔧</div>
          <div class="flow-node-title">Preprocess</div>
          <div class="flow-node-sub">Norm & Trim</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-node">
          <div class="flow-node-icon">📊</div>
          <div class="flow-node-title">MFCC</div>
          <div class="flow-node-sub">13 coeff</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-node">
          <div class="flow-node-icon">🧠</div>
          <div class="flow-node-title">CNN Model</div>
          <div class="flow-node-sub">Inferensi</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-node">
          <div class="flow-node-icon">📝</div>
          <div class="flow-node-title">Teks Output</div>
          <div class="flow-node-sub">Prediksi</div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="flow-node">
          <div class="flow-node-icon">🔊</div>
          <div class="flow-node-title">TTS Audio</div>
          <div class="flow-node-sub">edge-tts</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Module status
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3, gap="medium")
    for col, title, icon, status, color in [
        (s1, "ASR Module", "🎤", asr_status, "#10B981" if ASR_AVAILABLE else "#F43F5E"),
        (s2, "TTS Module", "🔊", tts_status, "#10B981" if TTS_AVAILABLE else "#F43F5E"),
        (s3, "CNN Model",  "🧠", model_st,   "#10B981" if (ASR_AVAILABLE and is_model_available()) else "#F59E0B"),
    ]:
        with col:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:24px 16px;">
              <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
              <div style="font-size:0.82rem; font-weight:700; text-transform:uppercase;
                          letter-spacing:0.08em; color:var(--text-4); margin-bottom:6px;">
                {title}
              </div>
              <div style="font-size:0.95rem; font-weight:600; color:{color};">{status}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ASR
# ══════════════════════════════════════════════════════════════════════════════
def page_asr():
    st.markdown("""
    <div class="page-header">
      <div class="section-label">AI · Speech Recognition</div>
      <div class="page-title">🎤 Automatic Speech Recognition</div>
      <div class="page-sub">
        Rekam langsung dari mikrofon atau upload file audio WAV — sistem memprediksi
        nama menggunakan Neural Network berbasis fitur MFCC 13 koefisien.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not ASR_AVAILABLE:
        st.error(f"❌ Modul ASR tidak tersedia: {ASR_ERROR}")
        return

    model_ready = is_model_available()
    if not model_ready:
        st.markdown("""
        <div class="demo-notice">
          <span style="font-size:1.2rem;">⚠️</span>
          <div>
            <strong>Mode Demo Aktif</strong> — File <code>asr/model/model_asr.h5</code>
            belum ditemukan. Prediksi menggunakan distribusi acak. Jalankan training di
            Google Colab dan letakkan model di <code>asr/model/model_asr.h5</code>
            untuk hasil nyata.
          </div>
        </div>
        """, unsafe_allow_html=True)

    tab_mic, tab_upload, tab_info = st.tabs([
        "🎙️  Rekam Langsung",
        "📂  Upload Audio",
        "📋  Panduan Dataset",
    ])

    # ── Tab 1: Mic ────────────────────────────────────────────────────────────
    with tab_mic:
        col_main, col_side = st.columns([3, 2], gap="large")

        with col_main:
            st.markdown("""
            <div class="glass-card-accent" style="text-align:center; margin-bottom:24px; padding:36px 24px;">
              <div class="section-label" style="margin-bottom:6px;">Langkah 1</div>
              <div style="font-size:1.05rem; font-weight:700; color:var(--text); margin-bottom:6px;">
                Rekam Suara dari Mikrofon
              </div>
              <div style="font-size:0.88rem; color:var(--text-3); line-height:1.6;">
                Klik 🎙️ untuk mulai → ucapkan nama → klik ⏹️ stop
              </div>
            </div>
            """, unsafe_allow_html=True)

            audio_recorded = st.audio_input(
                "Klik 🎙️ untuk mulai merekam, klik ⏹️ untuk berhenti",
                key="mic_recorder",
            )

            if audio_recorded is not None:
                audio_bytes = audio_recorded.read()
                st.markdown("""
                <div style="font-size:0.82rem; font-weight:700; text-transform:uppercase;
                            letter-spacing:0.1em; color:var(--text-4); margin:16px 0 6px;">
                  ▶️ Rekaman Anda
                </div>
                """, unsafe_allow_html=True)
                st.audio(audio_bytes, format="audio/wav")

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("🚀 Analisis & Prediksi", type="primary",
                             use_container_width=True, key="btn_mic_predict"):
                    with st.spinner("Memproses audio dan menjalankan model..."):
                        render_prediction(audio_bytes, model_ready)
            else:
                st.markdown("""
                <div style="background:var(--surface); border:1.5px dashed var(--border-2);
                            border-radius:var(--r-lg); padding:44px; text-align:center;
                            color:var(--text-4); font-size:0.9rem; margin-top:8px;">
                  <div style="font-size:2rem; margin-bottom:10px;">🎙️</div>
                  Belum ada rekaman.<br>
                  <span style="font-size:0.8rem;">
                    Klik tombol mikrofon di atas untuk mulai merekam.
                  </span>
                </div>
                """, unsafe_allow_html=True)

        with col_side:
            st.markdown("""
            <div class="settings-label">Kelas yang Didukung</div>
            """, unsafe_allow_html=True)

            for lbl in LABELS:
                st.markdown(f"""
                <div style="background:var(--surface-2); border:1px solid var(--border);
                            border-radius:9px; padding:9px 14px; margin-bottom:6px;
                            font-size:0.88rem; font-weight:600; color:var(--text-3);
                            transition:all 0.2s;">
                  📌 {lbl.capitalize()}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:18px;">
              <div class="settings-label">Tips Rekam</div>
              <div style="font-size:0.85rem; color:var(--text-3); line-height:2;">
                ✅ Izinkan akses mikrofon browser<br>
                ✅ Rekam di tempat senyap<br>
                ✅ Durasi cukup 1–2 detik<br>
                ✅ Ucapkan nama dengan jelas<br>
                ✅ Jarak mikrofon ±20–30 cm
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Upload ─────────────────────────────────────────────────────────
    with tab_upload:
        col_main, col_side = st.columns([3, 2], gap="large")

        with col_main:
            st.markdown("""
            <div style="font-size:0.82rem; font-weight:700; text-transform:uppercase;
                        letter-spacing:0.1em; color:var(--text-4); margin-bottom:12px;">
              Upload File Audio
            </div>
            """, unsafe_allow_html=True)

            uploaded = st.file_uploader(
                "Pilih file audio WAV / MP3 / OGG (16kHz, 1–2 detik)",
                type=["wav","WAV","mp3","ogg"],
                help="Format terbaik: WAV mono 16kHz",
                key="file_uploader",
            )

            if uploaded:
                audio_bytes = uploaded.read()
                st.audio(audio_bytes, format="audio/wav")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                if st.button("🚀 Analisis & Prediksi", type="primary",
                             use_container_width=True, key="btn_upload_predict"):
                    with st.spinner("Memproses audio..."):
                        render_prediction(audio_bytes, model_ready)
            else:
                st.markdown("""
                <div style="background:var(--surface); border:1.5px dashed var(--border-2);
                            border-radius:var(--r-lg); padding:44px; text-align:center;
                            color:var(--text-4); font-size:0.9rem; margin-top:8px;">
                  <div style="font-size:2rem; margin-bottom:10px;">📂</div>
                  Belum ada file dipilih.<br>
                  <span style="font-size:0.8rem;">Klik Browse files untuk upload.</span>
                </div>
                """, unsafe_allow_html=True)

        with col_side:
            st.markdown("""
            <div class="settings-label">Kelas yang Didukung</div>
            """, unsafe_allow_html=True)
            for lbl in LABELS:
                st.markdown(f"""
                <div style="background:var(--surface-2); border:1px solid var(--border);
                            border-radius:9px; padding:9px 14px; margin-bottom:6px;
                            font-size:0.88rem; font-weight:600; color:var(--text-3);">
                  📌 {lbl.capitalize()}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card" style="padding:18px; margin-top:16px;">
              <div class="settings-label">Format yang Didukung</div>
              <div style="font-size:0.85rem; color:var(--text-3); line-height:2;">
                ✅ WAV mono 16000 Hz<br>
                ✅ MP3<br>
                ✅ OGG<br>
                ✅ Durasi 1–2 detik<br>
                ✅ Suara jernih, minim noise
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Info ───────────────────────────────────────────────────────────
    with tab_info:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown("""
            <div class="section-label">Struktur Data</div>
            """, unsafe_allow_html=True)
            st.code("""dataset/
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
└── maria/         (40-50 file .wav)""", language="text")

        with c2:
            st.markdown("""
            <div class="section-label">Arsitektur CNN 1D</div>
            """, unsafe_allow_html=True)
            st.code("""Input: (batch, 32, 13)
  ↓
Conv1D(32, k=3, relu, same)
MaxPooling1D(2)
  ↓
Conv1D(64, k=3, relu, same)
MaxPooling1D(2)
  ↓
Flatten()
Dense(128, relu)
Dropout(0.3)
  ↓
Dense(12, softmax)

Optimizer: Adam
Loss: sparse_categorical_crossentropy""", language="text")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TTS
# ══════════════════════════════════════════════════════════════════════════════
def page_tts():
    st.markdown("""
    <div class="page-header">
      <div class="section-label">AI · Text-to-Speech</div>
      <div class="page-title">🔊 Neural Text-to-Speech</div>
      <div class="page-sub">
        Konversi teks Bahasa Indonesia menjadi suara natural menggunakan
        Microsoft Neural TTS. Pilih voice, atur kecepatan & volume, lalu download MP3.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not TTS_AVAILABLE:
        st.error(f"❌ Modul TTS tidak tersedia: {TTS_ERROR}")
        return

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        # ASR carry-over
        asr_text = st.session_state.get("asr_text", "")
        if asr_text:
            st.markdown("""
            <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25);
                        border-radius:10px; padding:10px 16px; margin-bottom:14px;
                        font-size:0.85rem; color:#34D399;">
              ✅ Hasil ASR tersedia — teks di bawah diisi dari prediksi ASR
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="settings-label">Teks Input</div>
        """, unsafe_allow_html=True)

        text_input = st.text_area(
            "Masukkan teks:",
            value=asr_text if asr_text else "Halo, selamat datang di SuaraKita. Platform ASR dan TTS Bahasa Indonesia berbasis kecerdasan buatan.",
            height=200,
            placeholder="Ketik teks Bahasa Indonesia di sini...",
            label_visibility="collapsed",
        )

        char_count = len(text_input)
        st.caption(f"🌍 Bahasa Indonesia, English, Japanese, Korean &nbsp;·&nbsp; {char_count} karakter")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🎵 Generate Suara", type="primary", use_container_width=True):
            if not text_input.strip():
                st.warning("⚠️ Teks tidak boleh kosong!")
            else:
                with st.spinner("Menghasilkan audio neural... ⏳"):
                    try:
                        voice_id   = st.session_state.get("tts_voice",  "id-ID-GadisNeural")
                        speed_val  = st.session_state.get("tts_speed",  "+0%")
                        volume_val = st.session_state.get("tts_volume", "+0%")

                        audio_bytes = generate_speech_bytes(
                            text_input, voice=voice_id,
                            rate=speed_val, volume=volume_val,
                        )

                        st.markdown("""
                        <div style="background:rgba(16,185,129,0.08);
                                    border:1px solid rgba(16,185,129,0.25);
                                    border-radius:var(--r-md); padding:20px; margin:16px 0;">
                          <div style="font-weight:700; color:#34D399; margin-bottom:14px;
                                      font-size:0.9rem;">
                            ✅ Audio berhasil dibuat!
                          </div>
                        """, unsafe_allow_html=True)

                        st.audio(audio_bytes, format="audio/mp3")

                        st.download_button(
                            "⬇️ Download MP3",
                            data=audio_bytes,
                            file_name=f"suarakita_{int(time.time())}.mp3",
                            mime="audio/mpeg",
                            use_container_width=True,
                        )
                        st.markdown("</div>", unsafe_allow_html=True)

                        st.session_state["tts_last_audio"] = audio_bytes
                        st.session_state["tts_last_text"]  = text_input

                    except Exception as e:
                        st.error(f"❌ Gagal generate audio: {e}")
                        st.exception(e)

        # Example texts
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="settings-label">Contoh Teks Cepat</div>', unsafe_allow_html=True)
        examples = [
            "Aku imut, lucu, dan menggemaskan.",
            "Selamat pagi, hari ini cuacanya cerah.",
            "Hello everyone, this is SuaraKita AI.",
            "Artificial intelligence is amazing.",
            "こんにちは、元気ですか？",
        ]
        for ex in examples:
            label = f'"{ex[:40]}…"' if len(ex) > 40 else f'"{ex}"'
            if st.button(label, use_container_width=True, key=f"ex_{ex[:15]}"):
                st.session_state["tts_example_text"] = ex
                st.rerun()

        if "tts_example_text" in st.session_state:
            st.info(f"💡 Salin: *{st.session_state['tts_example_text']}*")

    with col_right:
        st.markdown('<div class="settings-label">Pengaturan Voice</div>', unsafe_allow_html=True)

        # Voice selection
        voice_names = list_voices()
        sel_voice = st.selectbox("🌍 Pilih Voice", voice_names, index=0)
        voice_id  = get_voice_id(sel_voice)
        st.session_state["tts_voice"] = voice_id

        is_female = "Female" in sel_voice or "Perempuan" in sel_voice or "Gadis" in sel_voice
        badge_color = "#EC4899" if is_female else "#3B82F6"
        badge_icon  = "♀️" if is_female else "♂️"
        st.markdown(f"""
        <div class="voice-badge" style="background:rgba({'236,72,153' if is_female else '59,130,246'},0.1);
             border:1px solid rgba({'236,72,153' if is_female else '59,130,246'},0.3);
             color:{badge_color};">
          {badge_icon} <code style="color:{badge_color}; background:transparent;">{voice_id}</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Speed
        speed_names = list_speeds()
        sel_speed   = st.selectbox("⚡ Kecepatan Bicara", speed_names, index=1)
        speed_val   = get_speed_value(sel_speed)
        st.session_state["tts_speed"] = speed_val

        # Volume
        vol_names = list_volumes()
        sel_vol   = st.selectbox("🔉 Volume", vol_names, index=1)
        vol_val   = get_volume_value(sel_vol)
        st.session_state["tts_volume"] = vol_val

        # Active config
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card" style="padding:18px;">
          <div class="settings-label">Konfigurasi Aktif</div>
          <div style="font-size:0.85rem; line-height:2.2; color:var(--text-2);">
            🎤 Voice &nbsp;&nbsp;
              <code style="background:var(--surface-3); padding:2px 8px; border-radius:5px;
                           font-size:0.78rem; color:#60A5FA;">{voice_id}</code><br>
            ⚡ Rate &nbsp;&nbsp;&nbsp;
              <code style="background:var(--surface-3); padding:2px 8px; border-radius:5px;
                           font-size:0.78rem; color:#34D399;">{speed_val}</code><br>
            🔉 Vol &nbsp;&nbsp;&nbsp;&nbsp;
              <code style="background:var(--surface-3); padding:2px 8px; border-radius:5px;
                           font-size:0.78rem; color:#A78BFA;">{vol_val}</code>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ASR shortcut
        if st.session_state.get("asr_result"):
            st.markdown(f"""
            <div class="glass-card" style="padding:16px; margin-top:16px;
                 border-color:rgba(16,185,129,0.25);">
              <div class="settings-label">Dari ASR</div>
              <div style="font-size:0.9rem; color:#34D399; font-weight:600;">
                🎙️ {st.session_state['asr_result'].capitalize()}
              </div>
              <div style="font-size:0.8rem; color:var(--text-4); margin-top:4px;">
                Terdeteksi dari rekaman terakhir
              </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
def page_about():
    st.markdown("""
    <div class="page-header">
      <div class="section-label">Proyek · Deep Learning</div>
      <div class="page-title">ℹ️ Tentang SuaraKita</div>
      <div class="page-sub">
        Proyek akhir berbasis Deep Learning — ASR & TTS Bahasa Indonesia
        menggunakan CNN, MFCC, dan Microsoft Neural TTS.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-blue">🧠</div>
          <div class="feat-title">Teknologi ASR</div>
          <div class="tech-grid">
            <div class="tech-pill">Librosa</div>
            <div class="tech-pill">TensorFlow</div>
            <div class="tech-pill">Keras</div>
            <div class="tech-pill">NumPy</div>
            <div class="tech-pill">scikit-learn</div>
            <div class="tech-pill">Matplotlib</div>
            <div class="tech-pill">soundfile</div>
            <div class="tech-pill">Colab</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-purple">📊</div>
          <div class="feat-title">Pipeline ASR</div>
          <div style="font-size:0.88rem; color:var(--text-3); line-height:2.2;">
            1️⃣ Input audio (Mikrofon / WAV 16kHz)<br>
            2️⃣ Normalisasi &amp; Trim silence<br>
            3️⃣ Pad/Truncate → 2 detik<br>
            4️⃣ Ekstraksi MFCC (13 koef, 32 frame)<br>
            5️⃣ Inferensi CNN 1D model<br>
            6️⃣ Output: nama + confidence score
          </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-cyan">🔊</div>
          <div class="feat-title">Teknologi TTS</div>
          <div class="tech-grid">
            <div class="tech-pill">edge-tts</div>
            <div class="tech-pill">asyncio</div>
            <div class="tech-pill">pydub</div>
            <div class="tech-pill">MP3</div>
            <div class="tech-pill">Neural TTS</div>
            <div class="tech-pill">Multilingual</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="feat-icon feat-icon-green">🏗️</div>
          <div class="feat-title">Struktur Proyek</div>
        """, unsafe_allow_html=True)
        st.code("""speech-app/
├── app.py
├── requirements.txt
├── asr/
│   ├── preprocess.py
│   ├── feature_extraction.py
│   ├── predict.py
│   ├── utils.py
│   └── model/model_asr.h5
└── tts/
    ├── generate.py
    └── voices.py""", language="text")
        st.markdown("</div>", unsafe_allow_html=True)

    # Dataset specs
    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Spesifikasi Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
      <div class="spec-grid">
        <div class="spec-item">
          <div class="spec-val">12</div>
          <div class="spec-lbl">Kelas Nama</div>
        </div>
        <div class="spec-item">
          <div class="spec-val">500+</div>
          <div class="spec-lbl">Total Audio</div>
        </div>
        <div class="spec-item">
          <div class="spec-val">16kHz</div>
          <div class="spec-lbl">Sample Rate</div>
        </div>
        <div class="spec-item">
          <div class="spec-val">1–2s</div>
          <div class="spec-lbl">Durasi</div>
        </div>
        <div class="spec-item">
          <div class="spec-val">WAV</div>
          <div class="spec-lbl">Format</div>
        </div>
        <div class="spec-item">
          <div class="spec-val">CNN</div>
          <div class="spec-lbl">Arsitektur</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # GitHub
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:32px;">
      <div style="font-size:2rem; margin-bottom:10px;">🐙</div>
      <div style="font-weight:700; font-size:1rem; color:var(--text); margin-bottom:6px;">
        Version Control
      </div>
      <div style="font-size:0.9rem; color:var(--text-3); margin-bottom:18px;">
        Dikelola menggunakan GitHub untuk kolaborasi tim.
      </div>
      <code style="font-family:'JetBrains Mono',monospace; font-size:0.9rem; color:#60A5FA;
                   background:var(--surface-3); padding:10px 18px; border-radius:8px;
                   display:inline-block;">
        git clone https://github.com/asri20/suarakita-asr-tts
      </code>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

topnav()

page = st.session_state.page
if page == "home":
    page_home()
elif page == "asr":
    page_asr()
elif page == "tts":
    page_tts()
elif page == "about":
    page_about()
else:
    page_home()

st.markdown('</div>', unsafe_allow_html=True)