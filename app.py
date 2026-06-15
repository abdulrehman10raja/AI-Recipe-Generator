import streamlit as st
from groq import Groq, RateLimitError, AuthenticationError, APIConnectionError
from dotenv import load_dotenv
import os
import re
import base64
import html as html_mod
import datetime

# ─────────────────────────────────────────────
#  Load env & page config
# ─────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="Chef AI — by Abdul Rehman Raja",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
for _k, _v in [
    ("page", "splash"),
    ("recipe_history", []),
    ("chat_history", []),
    ("current_recipe", None),
    ("current_recipe_name", None),
    ("view_recipe_id", None),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────
#  GLOBAL CSS — Michelin-Star Kitchen Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600;1,700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&display=swap');

:root {
    --ink-deep:      #0A0806;
    --ink-dark:      #120E0A;
    --ink-mid:       #1C1610;
    --ink-surface:   #241C14;
    --ink-raised:    #2C2218;
    --ink-border:    rgba(196,148,68,0.20);
    --ink-border-hi: rgba(196,148,68,0.42);
    --amber:         #C49444;
    --amber-bright:  #D4A850;
    --amber-glow:    rgba(196,148,68,0.14);
    --amber-strong:  rgba(196,148,68,0.55);
    --cream:         #EAE0D0;
    --cream-soft:    #C8B898;
    --cream-muted:   #8A7A62;
    --cream-faint:   #3E3228;
    --emerald:       #2A7050;
    --emerald-dim:   rgba(42,112,80,0.22);
    --emerald-glow:  rgba(42,112,80,0.12);
    --rouge:         #8C2A1E;
    --rouge-glow:    rgba(140,42,30,0.15);
}

* { box-sizing: border-box; scroll-behavior: smooth; }

html, body {
    background: var(--ink-deep) !important;
    color: var(--cream) !important;
    min-height: 100vh;
    overflow-x: hidden;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
.main, section.main > div, .appview-container {
    background: transparent !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 5rem !important;
    max-width: 860px !important;
    position: relative;
    z-index: 10;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--ink-deep); }
::-webkit-scrollbar-thumb { background: var(--amber); border-radius: 3px; }

@keyframes candleFlicker {
    0%,100% { opacity:0.80; transform:scaleY(1) scaleX(1); }
    18%      { opacity:0.95; transform:scaleY(1.14) scaleX(0.88); }
    36%      { opacity:0.75; transform:scaleY(0.92) scaleX(1.10); }
    55%      { opacity:0.92; transform:scaleY(1.10) scaleX(0.93); }
    74%      { opacity:0.78; transform:scaleY(0.96) scaleX(1.06); }
}
@keyframes steamRise {
    0%   { transform:translateY(0) scaleX(1.0);   opacity:0.50; }
    45%  { transform:translateY(-52px) scaleX(1.4); opacity:0.22; }
    100% { transform:translateY(-110px) scaleX(0.6); opacity:0; }
}
@keyframes ambientPulse {
    0%,100% { opacity:0.55; }
    50%      { opacity:0.85; }
}
@keyframes goldShimmer {
    0%   { background-position:-240% center; }
    100% { background-position:240% center; }
}
@keyframes borderGlow {
    0%,100% { box-shadow:0 0 0 rgba(196,148,68,0), 0 8px 40px rgba(0,0,0,0.65); }
    50%      { box-shadow:0 0 28px rgba(196,148,68,0.12), 0 8px 40px rgba(0,0,0,0.65); }
}
@keyframes plateReveal {
    from { opacity:0; transform:translateY(20px) scale(0.97); }
    to   { opacity:1; transform:translateY(0)   scale(1); }
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(14px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn {
    from { opacity:0; }
    to   { opacity:1; }
}
@keyframes robotBob {
    0%,100% { transform:translateY(0); }
    50%      { transform:translateY(-10px); }
}
@keyframes splashBorderRun {
    0%   { background-position:0% 50%; }
    100% { background-position:300% 50%; }
}
@keyframes titleReveal {
    0%   { opacity:0; letter-spacing:18px; filter:blur(5px); }
    100% { opacity:1; letter-spacing:4px;  filter:blur(0); }
}
@keyframes scanPass {
    0%   { left:-20%; opacity:0; }
    10%  { opacity:0.6; }
    90%  { opacity:0.6; }
    100% { left:120%;  opacity:0; }
}
@keyframes crownPulse {
    0%,100% { text-shadow:0 0 8px rgba(196,148,68,0.4); }
    50%      { text-shadow:0 0 22px rgba(196,148,68,0.8), 0 0 40px rgba(196,148,68,0.3); }
}
@keyframes dotBlink {
    0%,100% { opacity:1; }
    50%      { opacity:0.2; }
}
@keyframes ringOrbit {
    from { transform:rotate(0deg); }
    to   { transform:rotate(360deg); }
}
@keyframes ringOrbitReverse {
    from { transform:rotate(360deg); }
    to   { transform:rotate(0deg); }
}
@keyframes cornerHud {
    0%,100% { opacity:0.85; }
    50%      { opacity:0.35; }
}
@keyframes tagAppear {
    0%   { opacity:0; transform:scale(0.8) translateY(6px); }
    60%  { transform:scale(1.05) translateY(-1px); }
    100% { opacity:1; transform:scale(1) translateY(0); }
}
@keyframes skeletonShimmer {
    0%   { background-position:-450px 0; }
    100% { background-position:450px 0; }
}
@keyframes sidebarSlideIn {
    from { opacity:0; transform:translateX(-14px); }
    to   { opacity:1; transform:translateX(0); }
}
@keyframes historyGlow {
    0%,100% { box-shadow: inset 0 0 0 1px rgba(196,148,68,0.18); }
    50%      { box-shadow: inset 0 0 14px rgba(196,148,68,0.10), inset 0 0 0 1px rgba(196,148,68,0.32); }
}
@keyframes activePulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(196,148,68,0.35); }
    50%      { box-shadow: 0 0 0 4px rgba(196,148,68,0.06); }
}

.kitchen-canvas {
    position:fixed; top:0; left:0;
    width:100vw; height:100vh;
    z-index:0; pointer-events:none; overflow:hidden;
}

/* ── SPLASH ── */
.splash-root {
    width:100%; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    padding:2rem 1.5rem 2rem; text-align:center;
    z-index:20; overflow-x:hidden;
}
.sp-hud { position:fixed; width:64px; height:64px; pointer-events:none; z-index:5; }
.sp-hud.tl { top:20px; left:20px; border-top:1.5px solid rgba(196,148,68,0.6); border-left:1.5px solid rgba(196,148,68,0.6); animation:cornerHud 3.5s ease-in-out infinite 0s; }
.sp-hud.tr { top:20px; right:20px; border-top:1.5px solid rgba(196,148,68,0.6); border-right:1.5px solid rgba(196,148,68,0.6); animation:cornerHud 3.5s ease-in-out infinite 0.9s; }
.sp-hud.bl { bottom:20px; left:20px; border-bottom:1.5px solid rgba(196,148,68,0.6); border-left:1.5px solid rgba(196,148,68,0.6); animation:cornerHud 3.5s ease-in-out infinite 1.8s; }
.sp-hud.br { bottom:20px; right:20px; border-bottom:1.5px solid rgba(196,148,68,0.6); border-right:1.5px solid rgba(196,148,68,0.6); animation:cornerHud 3.5s ease-in-out infinite 2.7s; }

.sp-robot-wrap {
    position:relative; display:inline-flex;
    align-items:center; justify-content:center;
    margin-bottom:1.2rem;
    animation:robotBob 4s ease-in-out infinite;
}
.sp-robot-ring { position:absolute; border-radius:50%; border-style:dashed; }
.sp-ring-outer { width:165px; height:165px; border:1px dashed rgba(196,148,68,0.30); animation:ringOrbit 18s linear infinite; }
.sp-ring-mid   { width:140px; height:140px; border:1px dashed rgba(196,148,68,0.18); animation:ringOrbitReverse 12s linear infinite; }
.sp-ring-inner { width:115px; height:115px; border:1px solid rgba(196,148,68,0.10); animation:ringOrbit 8s linear infinite; }

.sp-badge-wrap {
    position:relative; display:inline-flex; padding:2px; border-radius:8px;
    background:linear-gradient(90deg, #8A6428, #C49444, #EAC870, #D4A850, #8A6428);
    background-size:300% 100%;
    animation:splashBorderRun 4s linear infinite, fadeUp 0.8s ease-out 0.3s backwards;
    margin-bottom:1.2rem;
}
.sp-badge-inner {
    background: var(--ink-dark); border-radius:6px;
    padding:2rem 3.6rem 2.2rem;
    position:relative; overflow:hidden; max-width:680px;
}
.sp-badge-inner::before {
    content:''; position:absolute; top:0; left:-40%; width:30%; height:100%;
    background:linear-gradient(90deg, transparent, rgba(196,148,68,0.12), transparent);
    animation:scanPass 3.5s ease-in-out infinite; transform:skewX(-20deg);
}
.sp-title-eyebrow {
    font-family:'DM Sans', sans-serif; font-size:0.65rem; letter-spacing:5px;
    text-transform:uppercase; color:var(--amber); margin-bottom:0.7rem;
    display:flex; align-items:center; justify-content:center; gap:10px; opacity:0.85;
}
.sp-title-eyebrow::before, .sp-title-eyebrow::after {
    content:''; width:36px; height:1px; background:linear-gradient(90deg, transparent, var(--amber));
}
.sp-title-eyebrow::after { background:linear-gradient(270deg, transparent, var(--amber)); }
.sp-title-main {
    font-family:'Playfair Display', serif; font-size:clamp(3.2rem,9vw,5.8rem);
    font-weight:800; line-height:0.95; letter-spacing:4px; color:transparent;
    background:linear-gradient(120deg, #8A6428 0%, #C49444 25%, #EAC870 48%, #D4A850 65%, #A87830 85%, #D4A850 100%);
    background-size:280% 100%; -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; animation:goldShimmer 5s linear infinite, titleReveal 1s ease-out 0.1s backwards;
    margin:0 0 0.3rem;
}
.sp-title-sub {
    font-family:'Cormorant Garamond', serif; font-size:clamp(0.95rem,2.5vw,1.2rem);
    font-style:italic; color:var(--cream-soft); letter-spacing:1px; margin-bottom:0.2rem;
    animation:fadeUp 0.8s ease-out 0.5s backwards;
}
.sp-badge-bar {
    width:90px; height:1.5px;
    background:linear-gradient(90deg, transparent, var(--amber-bright), transparent);
    margin:0.8rem auto 1.2rem; animation:ambientPulse 3s ease-in-out infinite;
}
.sp-badge-desc {
    font-family:'Cormorant Garamond', serif; font-size:clamp(0.95rem,1.8vw,1.08rem);
    color:var(--cream-muted); line-height:1.85; max-width:520px; margin:0 auto;
    animation:fadeUp 0.8s ease-out 0.6s backwards;
}
.sp-badge-desc strong { color:var(--cream-soft); font-weight:600; }
.sp-version-chip {
    display:inline-flex; align-items:center; gap:10px;
    border:1px solid rgba(196,148,68,0.28); border-radius:2px;
    padding:0.35rem 1.2rem; font-family:'DM Sans', sans-serif;
    font-size:0.64rem; letter-spacing:3.5px; text-transform:uppercase;
    color:rgba(196,148,68,0.75); margin-bottom:1.2rem;
    animation:fadeUp 0.8s ease-out 0.7s backwards;
}
.sp-version-dot { width:5px; height:5px; border-radius:50%; background:var(--emerald); animation:dotBlink 2s ease-in-out infinite; }
.sp-creator-wrap {
    position:relative; display:inline-flex; padding:1.5px; border-radius:8px;
    background:linear-gradient(135deg, rgba(196,148,68,0.5), rgba(42,112,80,0.35), rgba(196,148,68,0.3));
    background-size:200% 200%;
    animation:splashBorderRun 6s linear infinite, fadeUp 0.8s ease-out 0.9s backwards;
    margin-bottom:1.2rem;
}
.sp-creator-card {
    background:rgba(18,14,10,0.95); border-radius:7px; padding:1.1rem 2rem;
    display:flex; align-items:center; gap:1.2rem; text-align:left;
}
.sp-avatar-shell {
    position:relative; width:52px; height:52px;
    display:flex; align-items:center; justify-content:center;
}
.sp-avatar-shell::before {
    content:''; position:absolute; inset:-8px; border-radius:10px;
    border:1px dashed rgba(196,148,68,0.38); animation:ringOrbit 8s linear infinite;
}
.sp-avatar-shell::after {
    content:''; position:absolute; inset:-16px; border-radius:12px;
    border:1px dotted rgba(42,112,80,0.28); animation:ringOrbitReverse 12s linear infinite;
}
.sp-avatar {
    width:52px; height:52px; border-radius:6px;
    background:linear-gradient(135deg, #8A6428, #C49444, #2A7050);
    display:flex; align-items:center; justify-content:center;
    font-family:'Playfair Display', serif; font-size:1.1rem; font-weight:700; color:#EAE0D0;
    border:1px solid rgba(196,148,68,0.45); box-shadow:0 0 18px rgba(196,148,68,0.25);
    position:relative; z-index:1;
}
.sp-creator-name { font-family:'Playfair Display', serif; font-size:1rem; font-weight:600; color:var(--cream); letter-spacing:0.5px; margin-bottom:2px; }
.sp-creator-role { font-family:'DM Sans', sans-serif; font-size:0.67rem; color:var(--cream-muted); letter-spacing:2px; text-transform:uppercase; margin-bottom:0.45rem; }
.sp-tags { display:flex; gap:0.4rem; flex-wrap:wrap; }
.sp-tag { font-family:'DM Sans', sans-serif; font-size:0.58rem; padding:2px 9px; border:1px solid; border-radius:2px; letter-spacing:1px; text-transform:uppercase; font-weight:500; }
.sp-tag-amber { border-color:rgba(196,148,68,0.45); color:var(--amber); animation:tagAppear 0.5s ease-out 1.2s backwards; }
.sp-tag-green { border-color:rgba(42,112,80,0.45); color:#4ABA80; animation:tagAppear 0.5s ease-out 1.35s backwards; }
.sp-tag-cream { border-color:rgba(200,184,152,0.35); color:var(--cream-soft); animation:tagAppear 0.5s ease-out 1.5s backwards; }
.sp-cta-hint { font-family:'DM Sans', sans-serif; font-size:0.6rem; color:rgba(196,148,68,0.35); letter-spacing:4px; text-transform:uppercase; margin-top:0.7rem; animation:dotBlink 3s ease-in-out infinite; }

/* ── MAIN ── */
.main-hero { text-align:center; padding:3.5rem 1.5rem 2rem; position:relative; }
.main-title {
    font-family:'Playfair Display', serif !important; font-size:clamp(2.8rem,7vw,4.8rem) !important;
    font-weight:800 !important; line-height:1 !important; color:transparent !important;
    background:linear-gradient(120deg, #8A6428 0%, #C49444 22%, #EAC870 46%, #D4A850 65%, #9A7430 85%, #D4A850 100%) !important;
    background-size:280% 100% !important; -webkit-background-clip:text !important;
    -webkit-text-fill-color:transparent !important; background-clip:text !important;
    animation:goldShimmer 5s linear infinite !important; margin:0 0 0.4rem !important; letter-spacing:3px !important;
}
.main-rule { display:flex; align-items:center; justify-content:center; gap:14px; margin:0.8rem 0; }
.main-rule-line { width:70px; height:1px; background:linear-gradient(90deg, transparent, rgba(196,148,68,0.5)); }
.main-rule-line.r { background:linear-gradient(270deg, transparent, rgba(196,148,68,0.5)); }
.main-rule-icon { font-size:0.8rem; color:var(--amber); opacity:0.75; }
.main-tagline { font-family:'Cormorant Garamond', serif; font-size:clamp(1rem,2.5vw,1.2rem); font-style:italic; color:var(--cream-soft); letter-spacing:0.5px; margin-bottom:0.4rem; }
.main-credit { font-family:'DM Sans', sans-serif; font-size:0.68rem; letter-spacing:3.5px; text-transform:uppercase; color:var(--cream-faint); opacity:0.85; }

.section-card {
    background: linear-gradient(145deg, rgba(28,22,16,0.92) 0%, rgba(20,16,10,0.95) 100%) !important;
    border: 1px solid var(--ink-border) !important; border-radius: 4px !important;
    padding: 1.7rem 2rem !important; margin-bottom: 1.2rem !important;
    backdrop-filter: blur(18px) !important; -webkit-backdrop-filter: blur(18px) !important;
    animation: borderGlow 5s ease-in-out infinite, plateReveal 0.5s ease-out backwards !important;
    position: relative !important; overflow: hidden !important;
}
.section-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg, transparent, var(--amber-strong), transparent);
}
.section-card::after {
    content:''; position:absolute; bottom:6px; right:8px;
    width:10px; height:10px;
    border-bottom:1px solid rgba(196,148,68,0.25); border-right:1px solid rgba(196,148,68,0.25);
}
.section-label {
    font-family:'DM Sans', sans-serif !important; font-size:0.68rem !important;
    letter-spacing:4px !important; text-transform:uppercase !important;
    color:var(--amber) !important; margin-bottom:1rem !important;
    display:flex !important; align-items:center !important; gap:10px !important;
}
.section-label::after { content:'' !important; flex:1 !important; height:1px !important; background:linear-gradient(90deg, rgba(196,148,68,0.30), transparent) !important; }

/* ── INPUTS ── */
.stTextArea textarea {
    background: rgba(10,8,5,0.90) !important; border: 1.5px solid var(--ink-border) !important;
    border-radius: 3px !important; color: var(--cream) !important;
    font-family: 'Cormorant Garamond', serif !important; font-size: 1.05rem !important;
    resize: none !important; transition: all 0.3s ease !important; caret-color: var(--amber-bright) !important;
    padding: 14px 16px !important; line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: var(--ink-border-hi) !important;
    box-shadow: 0 0 0 3px rgba(196,148,68,0.08), 0 0 24px rgba(196,148,68,0.06) !important;
    background: rgba(14,11,7,0.95) !important;
}
.stTextArea textarea::placeholder { color: var(--cream-faint) !important; font-style: italic !important; font-family: 'Cormorant Garamond', serif !important; font-size: 0.95rem !important; }
.stTextArea label { display:none !important; }

.stSelectbox > div > div { background: rgba(10,8,5,0.90) !important; border: 1.5px solid var(--ink-border) !important; border-radius: 3px !important; color: var(--cream) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important; }
.stSelectbox label { font-family: 'DM Sans', sans-serif !important; font-size: 0.65rem !important; letter-spacing: 2.5px !important; text-transform: uppercase !important; color: var(--cream-muted) !important; font-weight: 500 !important; }

/* DROPDOWN DARK THEME */
[data-baseweb="select"] { background: transparent !important; }
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="popover"] > div > div, [data-baseweb="popover"] > div > div > div { background: #0D0A06 !important; border: 1px solid rgba(196,148,68,0.30) !important; border-radius: 4px !important; box-shadow: 0 12px 48px rgba(0,0,0,0.95), 0 0 0 1px rgba(196,148,68,0.10) !important; }
[data-baseweb="menu"], ul[data-baseweb="menu"], [role="listbox"] { background: #0D0A06 !important; border: none !important; padding: 4px 0 !important; }
[data-baseweb="option"], [role="option"], li[data-baseweb], li[role="option"] { background: transparent !important; color: #C8B898 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important; letter-spacing: 0.5px !important; padding: 10px 16px !important; border-left: 2px solid transparent !important; transition: all 0.18s ease !important; cursor: pointer !important; }
[data-baseweb="option"]:hover, [role="option"]:hover, li[data-baseweb]:hover, li[role="option"]:hover { background: rgba(196,148,68,0.10) !important; color: #D4A850 !important; border-left-color: rgba(196,148,68,0.55) !important; }
[data-baseweb="option"][aria-selected="true"], [role="option"][aria-selected="true"], [data-baseweb="option"][data-highlighted="true"] { background: rgba(196,148,68,0.14) !important; color: #EAC870 !important; border-left-color: #C49444 !important; }
[data-baseweb="popover"] * { background-color: transparent !important; }
[data-baseweb="popover"] [data-baseweb="option"], [data-baseweb="popover"] [role="option"], [data-baseweb="popover"] li { background-color: transparent !important; }
[data-baseweb="popover"] [data-baseweb="option"]:hover, [data-baseweb="popover"] [role="option"]:hover { background-color: rgba(196,148,68,0.10) !important; }
[data-baseweb="select"] [data-id], [data-baseweb="select"] span, [data-baseweb="select"] div { color: var(--cream) !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #8A6428 0%, #B48440 35%, #C49444 55%, #A07438 80%, #8A6428 100%) !important;
    background-size: 240% 100% !important; color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important;
    font-size: 0.78rem !important; letter-spacing: 4px !important; text-transform: uppercase !important;
    border: none !important; border-radius: 2px !important; padding: 1.05rem 2.2rem !important;
    width: 100% !important; transition: all 0.3s ease !important;
    box-shadow: 0 4px 28px rgba(196,148,68,0.22), 0 2px 8px rgba(0,0,0,0.65) !important;
    position: relative !important; overflow: hidden !important; text-shadow: 0 1px 3px rgba(0,0,0,0.50) !important;
}
.stButton > button::before { content: '' !important; position: absolute !important; top: 0 !important; left: -60% !important; width: 40% !important; height: 100% !important; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent) !important; transform: skewX(-20deg) !important; transition: left 0.5s ease !important; }
.stButton > button:hover::before { left: 150% !important; }
.stButton > button:hover { transform: translateY(-3px) !important; box-shadow: 0 10px 40px rgba(196,148,68,0.38), 0 4px 14px rgba(0,0,0,0.7) !important; background-position: right center !important; }
.stButton > button:active { transform: translateY(0) scale(0.99) !important; }
.stButton > button p, .stButton > button div, .stButton > button span { color:#FFFFFF !important; text-shadow: 0 1px 3px rgba(0,0,0,0.50) !important; }

.recipe-action-row .stButton > button { background: transparent !important; border: 1.5px solid var(--ink-border-hi) !important; color: var(--amber) !important; box-shadow: none !important; font-size: 0.7rem !important; letter-spacing: 2px !important; }
.recipe-action-row .stButton > button p, .recipe-action-row .stButton > button div, .recipe-action-row .stButton > button span { color: var(--amber) !important; }
.recipe-action-row .stButton > button:hover { background: rgba(196,148,68,0.08) !important; border-color: var(--amber-bright) !important; box-shadow: 0 0 18px rgba(196,148,68,0.15) !important; transform: translateY(-2px) !important; }

.stButton > button[kind="primary"] { background: linear-gradient(135deg, #8A6428 0%, #C49444 45%, #EAC870 62%, #C49444 80%, #8A6428 100%) !important; background-size: 240% 100% !important; box-shadow: 0 6px 36px rgba(196,148,68,0.30), 0 0 0 1px rgba(196,148,68,0.15) !important; font-size: 0.82rem !important; letter-spacing: 5px !important; border-radius: 3px !important; padding: 1.15rem 2.5rem !important; }
.stButton > button[kind="primary"]:hover { box-shadow: 0 12px 48px rgba(196,148,68,0.50), 0 0 0 1px rgba(196,148,68,0.30) !important; transform: translateY(-4px) !important; }
.stButton > button[kind="primary"] p, .stButton > button[kind="primary"] div, .stButton > button[kind="primary"] span { color: #FFFFFF !important; text-shadow: 0 1px 3px rgba(0,0,0,0.50) !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 3px !important; }
.stSuccess > div { background: rgba(18,50,36,0.40) !important; border: 1px solid rgba(42,112,80,0.42) !important; color: #6ADA9A !important; border-radius: 3px !important; }
.stWarning > div { background: rgba(100,64,8,0.28) !important; border: 1px solid rgba(196,148,68,0.40) !important; color: var(--amber-bright) !important; border-radius: 3px !important; }
.stError > div { background: rgba(90,22,14,0.28) !important; border: 1px solid rgba(160,50,40,0.40) !important; border-radius: 3px !important; }

/* ── DOWNLOAD ── */
.stDownloadButton > button { background: transparent !important; border: 1.5px solid var(--ink-border-hi) !important; color: var(--amber) !important; border-radius: 3px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.7rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; transition: all 0.22s ease !important; }
.stDownloadButton > button:hover { background: rgba(196,148,68,0.10) !important; border-color: var(--amber-bright) !important; transform: translateY(-1px) !important; }

.stSpinner > div { border-top-color: var(--amber) !important; }
hr { border-color: rgba(196,148,68,0.15) !important; }

.footer-wrap { text-align: center; padding: 2.5rem 0 1rem; border-top: 1px solid rgba(196,148,68,0.12); margin-top: 1.5rem; }
.footer-ornament { color: rgba(196,148,68,0.40); font-family: 'DM Sans', sans-serif; font-size: 0.65rem; letter-spacing: 7px; margin-bottom: 0.8rem; }
.footer-main { font-family: 'Playfair Display', serif; color: rgba(196,148,68,0.50); font-size: 1rem; font-weight: 700; letter-spacing: 4px; margin-bottom: 0.3rem; }
.footer-sub { color: rgba(62,50,40,0.90); font-family: 'DM Sans', sans-serif; font-size: 0.7rem; letter-spacing: 1px; }

.empty-hint { text-align: center; padding: 1.8rem 0; color: rgba(138,122,98,0.35); font-family: 'Cormorant Garamond', serif; font-size: 1rem; font-style: italic; letter-spacing: 1px; }

/* ── SKELETON ── */
.skel-root { animation: rvFadeUp 0.4s ease-out; padding: 0.5rem 0; }
.skel-block { background: linear-gradient(90deg, rgba(28,22,16,0.9) 0%, rgba(44,34,24,0.95) 50%, rgba(28,22,16,0.9) 100%); background-size: 900px 100%; animation: skeletonShimmer 1.6s linear infinite; border: 1px solid rgba(196,148,68,0.14); border-radius: 5px; margin-bottom: 0.85rem; }
.skel-title { height: 46px; width: 60%; margin: 0 auto 1.4rem; border-radius: 4px; }
.skel-line  { height: 16px; margin-bottom: 10px; border-radius: 3px; }
.skel-line.w90 { width:90%; } .skel-line.w75 { width:75%; } .skel-line.w60 { width:60%; }
.skel-card { height: 96px; } .skel-row  { height: 48px; margin-bottom: 8px; border-radius: 3px; }
.skel-eyebrow { text-align:center; font-family:'DM Sans',sans-serif; font-size:0.6rem; letter-spacing:5px; text-transform:uppercase; color:rgba(196,148,68,0.55); margin-bottom: 1rem; animation: dotBlink 1.6s ease-in-out infinite; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: linear-gradient(165deg, rgba(14,11,7,0.98) 0%, rgba(8,6,4,0.99) 100%) !important; border-right: 1px solid rgba(196,148,68,0.18) !important; }
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] .block-container { padding: 1.2rem 1rem 2rem !important; max-width: 100% !important; }

.hist-header { display:flex; align-items:center; gap:10px; padding: 0.4rem 0 1rem; border-bottom: 1px solid rgba(196,148,68,0.16); margin-bottom: 1rem; animation: sidebarSlideIn 0.45s ease-out backwards; }
.hist-header-icon { font-size: 1.3rem; filter: drop-shadow(0 0 8px rgba(196,148,68,0.5)); animation: crownPulse 3.5s ease-in-out infinite; }
.hist-header-text { font-family:'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: transparent; background: linear-gradient(120deg, #8A6428 0%, #C49444 30%, #EAC870 55%, #D4A850 80%, #8A6428 100%); background-size: 280% 100%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: goldShimmer 5s linear infinite; letter-spacing: 1px; }
.hist-header-count { margin-left:auto; font-family:'DM Sans', sans-serif; font-size: 0.62rem; letter-spacing: 1.5px; color: var(--amber); border: 1px solid rgba(196,148,68,0.32); border-radius: 20px; padding: 2px 9px; background: rgba(196,148,68,0.08); }
.hist-empty { text-align:center; padding: 2.2rem 0.6rem; font-family:'Cormorant Garamond', serif; font-style: italic; font-size: 0.95rem; color: rgba(138,122,98,0.45); line-height: 1.8; animation: fadeIn 0.6s ease-out; }
.hist-empty-icon { font-size: 1.8rem; display:block; margin-bottom:0.5rem; opacity:0.5; filter: drop-shadow(0 0 10px rgba(196,148,68,0.25)); }

.hist-card { position: relative; background: linear-gradient(145deg, rgba(24,18,12,0.92) 0%, rgba(14,11,7,0.96) 100%); border: 1px solid rgba(196,148,68,0.18); border-radius: 5px; padding: 0.85rem 0.95rem 0.8rem; margin-bottom: 0.65rem; overflow: hidden; transition: border-color 0.25s ease, transform 0.2s ease; animation: sidebarSlideIn 0.4s ease-out backwards, historyGlow 6s ease-in-out infinite; }
.hist-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1.5px; background: linear-gradient(90deg, transparent, rgba(196,148,68,0.55), transparent); }
.hist-card:hover { border-color: rgba(196,148,68,0.42); transform: translateX(2px); }
.hist-card.active { border-color: var(--amber-bright); animation: sidebarSlideIn 0.4s ease-out backwards, activePulse 2.4s ease-in-out infinite; }
.hist-card-top { display:flex; align-items:flex-start; justify-content:space-between; gap:8px; margin-bottom:0.35rem; }
.hist-card-name { font-family:'Playfair Display', serif; font-size: 0.92rem; font-weight: 700; color: var(--cream); line-height: 1.3; letter-spacing: 0.3px; }
.hist-card-badge { flex-shrink:0; font-family:'DM Sans', sans-serif; font-size: 0.55rem; letter-spacing: 1.5px; text-transform: uppercase; color: var(--amber); border: 1px solid rgba(196,148,68,0.32); border-radius: 2px; padding: 1px 6px; background: rgba(196,148,68,0.06); white-space: nowrap; }
.hist-card-meta { display:flex; align-items:center; gap:8px; flex-wrap:wrap; font-family:'DM Sans', sans-serif; font-size: 0.60rem; letter-spacing: 1px; text-transform: uppercase; color: var(--cream-muted); margin-bottom: 0.45rem; }
.hist-card-meta span { display:flex; align-items:center; gap:3px; }
.hist-card-time { font-family:'Cormorant Garamond', serif; font-size: 0.78rem; font-style: italic; color: rgba(196,148,68,0.55); letter-spacing: 0.5px; }
.hist-card-ing { font-family:'Cormorant Garamond', serif; font-size: 0.82rem; color: var(--cream-soft); line-height: 1.5; margin-top: 0.35rem; opacity: 0.85; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

section[data-testid="stSidebar"] .stButton > button { font-size: 0.62rem !important; letter-spacing: 2px !important; padding: 0.55rem 0.8rem !important; border-radius: 3px !important; }
section[data-testid="stSidebar"] .hist-card-actions .stButton > button { background: transparent !important; border: 1px solid rgba(196,148,68,0.28) !important; color: var(--amber) !important; box-shadow: none !important; font-size: 0.58rem !important; letter-spacing: 1.5px !important; padding: 0.4rem 0.6rem !important; width: 100% !important; }
section[data-testid="stSidebar"] .hist-card-actions .stButton > button:hover { background: rgba(196,148,68,0.10) !important; border-color: var(--amber-bright) !important; transform: none !important; box-shadow: 0 0 14px rgba(196,148,68,0.12) !important; }
.hist-clear-wrap .stButton > button { background: transparent !important; border: 1px solid rgba(140,42,30,0.35) !important; color: #C8645A !important; box-shadow: none !important; width: 100% !important; }
.hist-clear-wrap .stButton > button:hover { background: rgba(140,42,30,0.10) !important; border-color: rgba(196,90,75,0.55) !important; transform: none !important; }
.hist-new-wrap .stButton > button { width: 100% !important; margin-bottom: 1rem !important; }
.hist-footer { text-align:center; margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(196,148,68,0.12); font-family:'DM Sans', sans-serif; font-size: 0.56rem; letter-spacing: 4px; text-transform: uppercase; color: rgba(196,148,68,0.30); }

@media(max-width:640px) {
    .main-title { font-size: 2.6rem !important; }
    .sp-title-main { font-size: 2.8rem; }
    .sp-badge-inner { padding: 1.2rem 1.8rem; }
    .block-container { padding-left: 0.8rem !important; padding-right: 0.8rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GLOBAL ANIMATED BACKGROUND SVG
# ─────────────────────────────────────────────
st.markdown("""
<div class="kitchen-canvas" aria-hidden="true">
<svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice"
     xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%;">
  <defs>
    <radialGradient id="rg-candle" cx="8%" cy="85%" r="55%">
      <stop offset="0%"   stop-color="#C49444" stop-opacity=".18"/>
      <stop offset="100%" stop-color="#0A0806" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="rg-center" cx="50%" cy="60%" r="50%">
      <stop offset="0%"   stop-color="#1C1408" stop-opacity=".70"/>
      <stop offset="100%" stop-color="#0A0806" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="rg-top" cx="50%" cy="0%" r="40%">
      <stop offset="0%"   stop-color="#C49444" stop-opacity=".05"/>
      <stop offset="100%" stop-color="#0A0806" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="rg-vig" cx="50%" cy="50%" r="70%">
      <stop offset="0%"   stop-color="transparent"/>
      <stop offset="100%" stop-color="#040302" stop-opacity=".80"/>
    </radialGradient>
    <filter id="fblur"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="fblur2"><feGaussianBlur stdDeviation="12"/></filter>
  </defs>
  <rect width="1440" height="900" fill="#0A0806"/>
  <rect width="1440" height="900" fill="url(#rg-candle)"/>
  <rect width="1440" height="900" fill="url(#rg-center)"/>
  <rect width="1440" height="900" fill="url(#rg-top)"/>
  <g opacity=".035" stroke="#C49444" stroke-width="0.7">
    <line x1="0" y1="160" x2="1440" y2="160"/><line x1="0" y1="320" x2="1440" y2="320"/>
    <line x1="0" y1="480" x2="1440" y2="480"/><line x1="0" y1="640" x2="1440" y2="640"/>
    <line x1="240" y1="0" x2="240" y2="660"/><line x1="480" y1="0" x2="480" y2="660"/>
    <line x1="720" y1="0" x2="720" y2="660"/><line x1="960" y1="0" x2="960" y2="660"/>
    <line x1="1200" y1="0" x2="1200" y2="660"/>
  </g>
  <rect x="0" y="0" width="1440" height="88" fill="#0C0A07"/>
  <rect x="0" y="84" width="1440" height="8" fill="#161008" rx="2"/>
  <rect x="0" y="84" width="1440" height="1.5" fill="rgba(196,148,68,0.25)"/>
  <rect x="0" y="87" width="1440" height="0.8" fill="rgba(196,148,68,0.10)"/>
  <g>
    <rect x="84" y="22" width="36" height="54" rx="18" fill="#1E1610" stroke="rgba(196,148,68,0.3)" stroke-width="1.5"/>
    <ellipse cx="102" cy="24" rx="9" ry="7" fill="#C49444" opacity=".65" style="animation:ambientPulse 2.8s ease-in-out infinite"/>
    <ellipse cx="102" cy="90" rx="80" ry="65" fill="#C49444" opacity=".06" filter="url(#fblur)"/>
  </g>
  <g>
    <rect x="702" y="22" width="36" height="54" rx="18" fill="#1E1610" stroke="rgba(196,148,68,0.3)" stroke-width="1.5"/>
    <ellipse cx="720" cy="24" rx="9" ry="7" fill="#C49444" opacity=".70" style="animation:ambientPulse 2.8s ease-in-out infinite 0.4s"/>
    <ellipse cx="720" cy="90" rx="90" ry="70" fill="#C49444" opacity=".07" filter="url(#fblur)"/>
  </g>
  <g>
    <rect x="1318" y="22" width="36" height="54" rx="18" fill="#1E1610" stroke="rgba(196,148,68,0.3)" stroke-width="1.5"/>
    <ellipse cx="1336" cy="24" rx="9" ry="7" fill="#C49444" opacity=".65" style="animation:ambientPulse 2.8s ease-in-out infinite 0.8s"/>
    <ellipse cx="1336" cy="90" rx="80" ry="65" fill="#C49444" opacity=".06" filter="url(#fblur)"/>
  </g>
  <rect x="0" y="668" width="1440" height="232" fill="#0C0A07"/>
  <rect x="0" y="662" width="1440" height="12" fill="#181208" rx="3"/>
  <rect x="0" y="663" width="1440" height="1.5" fill="rgba(196,148,68,0.28)"/>
  <rect x="16" y="674" width="1408" height="220" fill="#0E0C08" rx="3"/>
  <g transform="translate(1300,700)">
    <ellipse cx="0" cy="42" rx="42" ry="17" fill="#6A3C18" stroke="#8A5428" stroke-width="2"/>
    <rect x="-42" y="-2" width="84" height="48" fill="#7A4A22" rx="3"/>
    <ellipse cx="0" cy="-2" rx="42" ry="17" fill="#9A6438" stroke="#B07848" stroke-width="2"/>
    <ellipse cx="0" cy="-6" rx="46" ry="12" fill="#C08040" opacity=".55"/>
    <circle cx="0" cy="-20" r="8" fill="#7A4A22" stroke="#9A6438" stroke-width="1.5"/>
    <line x1="-42" y1="22" x2="-65" y2="18" stroke="#6A3C18" stroke-width="6" stroke-linecap="round"/>
    <line x1="42" y1="22" x2="65" y2="18" stroke="#6A3C18" stroke-width="6" stroke-linecap="round"/>
    <g style="animation:steamRise 3.2s ease-in-out infinite; transform-origin:0px -10px;">
      <path d="M-8 -10 Q-14 -35 -8 -60 Q-2 -85 -8 -110" fill="none" stroke="rgba(210,195,175,0.32)" stroke-width="8" stroke-linecap="round"/>
    </g>
  </g>
  <rect x="0" y="862" width="1440" height="38" fill="#0A0806"/>
  <rect x="0" y="860" width="1440" height="1.5" fill="rgba(196,148,68,0.22)"/>
  <rect width="1440" height="900" fill="url(#rg-vig)"/>
  <rect x="0" y="0" width="1440" height="75" fill="#060402" opacity=".60"/>
</svg>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Robot Chef SVG (base64)
# ─────────────────────────────────────────────
_robot_svg = (
    '<svg width="160" height="230" viewBox="0 0 160 230" xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<radialGradient id="rg1" cx="50%" cy="30%" r="70%"><stop offset="0%" stop-color="#C49444"/><stop offset="100%" stop-color="#6A3C10"/></radialGradient>'
    '</defs>'
    '<style>'
    '@keyframes eyeB{0%,88%,100%{opacity:.90}91%{opacity:.08}94%{opacity:.85}}'
    '.ey{animation:eyeB 3.8s ease-in-out infinite}'
    '@keyframes antG{0%,100%{opacity:.9;r:10px}50%{opacity:.2;r:13px}}'
    '.ag{animation:antG 1.8s ease-in-out infinite}'
    '</style>'
    '<rect x="38" y="2" width="84" height="60" rx="10" fill="#F2F0EA" stroke="#D8D4CC" stroke-width="1.5"/>'
    '<rect x="30" y="58" width="100" height="16" rx="8" fill="#E8E4DC" stroke="#CCC8C0" stroke-width="1.5"/>'
    '<rect x="75" y="58" width="10" height="22" rx="5" fill="#A07040"/>'
    '<circle cx="80" cy="54" r="10" fill="#C49444"/>'
    '<circle cx="80" cy="54" r="5" fill="#EAC870" opacity=".90"/>'
    '<rect x="16" y="72" width="128" height="90" rx="14" fill="#8C9EB0" stroke="#6C8A9C" stroke-width="2.5"/>'
    '<rect x="24" y="80" width="112" height="76" rx="10" fill="#7C90A4" stroke="#5C7E92" stroke-width="1.5"/>'
    '<rect x="28" y="88" width="40" height="30" rx="8" fill="#060808" stroke="#C49444" stroke-width="2.5"/>'
    '<ellipse cx="48" cy="103" rx="13" ry="12" fill="#C49444" opacity=".90"/>'
    '<ellipse cx="48" cy="103" rx="8.5" ry="8" fill="#8A6420" opacity=".95"/>'
    '<circle cx="48" cy="103" r="5" fill="#1A0E04"/>'
    '<ellipse cx="52" cy="97.5" rx="3.5" ry="2.8" fill="rgba(255,255,255,0.92)"/>'
    '<ellipse cx="48" cy="103" rx="19" ry="17" fill="#C49444" opacity=".14" class="ey"/>'
    '<rect x="92" y="88" width="40" height="30" rx="8" fill="#060808" stroke="#C49444" stroke-width="2.5"/>'
    '<ellipse cx="112" cy="103" rx="13" ry="12" fill="#C49444" opacity=".90"/>'
    '<ellipse cx="112" cy="103" rx="8.5" ry="8" fill="#8A6420" opacity=".95"/>'
    '<circle cx="112" cy="103" r="5" fill="#1A0E04"/>'
    '<ellipse cx="116" cy="97.5" rx="3.5" ry="2.8" fill="rgba(255,255,255,0.92)"/>'
    '<ellipse cx="112" cy="103" rx="19" ry="17" fill="#C49444" opacity=".14" class="ey"/>'
    '<rect x="32" y="130" width="96" height="20" rx="10" fill="#040806" stroke="#C49444" stroke-width="1.8"/>'
    '<rect x="6" y="162" width="148" height="58" rx="12" fill="#F0EEE8" stroke="#D8D4CC" stroke-width="2"/>'
    '<path d="M58 162 L66 178 L80 174 L94 178 L102 162Z" fill="#E6E2DC" stroke="#D0CCC6" stroke-width="1"/>'
    '<rect x="90" y="170" width="48" height="28" rx="3" fill="#F8F6F2" stroke="#D8D4CC" stroke-width="1"/>'
    '<text x="94" y="181" font-size="7.5" fill="#8A6428" font-family="Georgia,serif" font-weight="bold" letter-spacing="0.5">CHEF</text>'
    '<text x="97" y="192" font-size="7.5" fill="#8A6428" font-family="Georgia,serif" font-weight="bold" letter-spacing="1.5">AI</text>'
    '<rect x="0" y="163" width="12" height="48" rx="6" fill="#8C9EB0" stroke="#6C8A9C" stroke-width="1.5"/>'
    '<circle cx="6" cy="208" r="10" fill="#7C90A4" stroke="#5C7E92" stroke-width="1.5"/>'
    '<rect x="148" y="163" width="12" height="46" rx="6" fill="#8C9EB0" stroke="#6C8A9C" stroke-width="1.5"/>'
    '<circle cx="154" cy="206" r="11" fill="#7C90A4" stroke="#5C7E92" stroke-width="1.5"/>'
    '<line x1="154" y1="198" x2="154" y2="224" stroke="#C49444" stroke-width="5" stroke-linecap="round"/>'
    '<ellipse cx="154" cy="228" rx="11" ry="8" fill="#C49444"/>'
    '</svg>'
)
_robot_b64 = base64.b64encode(_robot_svg.encode("utf-8")).decode("utf-8")

# ─────────────────────────────────────────────
#  API key
# ─────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("⚠️  API key not found. Add GROQ_API_KEY to your .env file and restart.")
    st.stop()

client = Groq(api_key=api_key)

# ════════════════════════════════════════════
#  CUISINE-SPECIFIC PROMPT NOTES
# ════════════════════════════════════════════
CUISINE_NOTES = {
    "Pakistani": "Use traditional spices like cumin, coriander, turmeric, garam masala, red chilli powder. Consider salan-style gravies, tarka (tempering) techniques, and balanced layering of spices.",
    "Arabic": "Use warm spices like cumin, cinnamon, sumac, za'atar, and seven-spice. Favor grilling, slow braising, and bright finishes like lemon and herbs.",
    "Chinese": "Use techniques like stir-frying on high heat, balancing soy, ginger, garlic, and a touch of sugar or vinegar for depth. Keep textures crisp where relevant.",
    "Italian": "Use classic Italian technique — don't over-spice. Let quality ingredients speak through olive oil, garlic, fresh herbs (basil, oregano), and simple reductions.",
    "Indian": "Use layered spice building (whole spices bloomed in oil, then ground spices), onion-tomato bases, and finishing touches like garam masala or fresh coriander.",
    "Mediterranean": "Use olive oil, lemon, garlic, fresh herbs (parsley, oregano, mint), and lighter grilling or roasting techniques with minimal heavy sauces.",
    "Thai": "Balance the four pillars — sweet, sour, salty, spicy — using fish sauce, lime, chilli, and palm sugar where appropriate, with fresh aromatics like lemongrass and Thai basil.",
}

# ════════════════════════════════════════════
#  INPUT VALIDATION
# ════════════════════════════════════════════
def validate_ingredients(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    if len(stripped) < 3:
        return False, "Please enter at least one ingredient to continue."
    if len(text) > 1000:
        return False, "Too many characters — keep your ingredient list under 1000 characters."
    if not re.search(r"[a-zA-Z]", text):
        return False, "Ingredients should contain letters — please describe what's in your fridge."
    return True, ""


# ════════════════════════════════════════════
#  RECIPE PARSER & RENDERER
# ════════════════════════════════════════════
def _parse_recipe(text: str) -> dict:
    sections = {}
    current_key = None
    current_lines = []
    for line in text.strip().split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = stripped[3:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()
    return sections


def _list_items(text: str) -> list:
    items = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^[\d]+[.)]\s*", "", line)
        cleaned = re.sub(r"^[-•*✦]\s*", "", cleaned)
        if cleaned:
            items.append(cleaned)
    return items


def _parse_times(text: str) -> dict:
    t = {}
    for line in text.split("\n"):
        ll = line.lower()
        val = re.sub(r"^[^:]*:\s*", "", line).strip().strip("[]")
        if "prep" in ll and val:
            t["prep"] = val
        elif "cook" in ll and val:
            t["cook"] = val
        elif "total" in ll and val:
            t["total"] = val
    return t


# Emoji lookup for nutrition labels (matched case-insensitively, substring match)
NUTRI_EMOJI_MAP = [
    ("calorie", "🔥"),
    ("kcal", "🔥"),
    ("protein", "🍗"),
    ("carb", "🍞"),
    ("fat", "🧈"),
    ("fiber", "🌾"),
    ("fibre", "🌾"),
    ("sugar", "🍯"),
    ("sodium", "🧂"),
    ("salt", "🧂"),
    ("cholesterol", "🥚"),
    ("vitamin", "🍊"),
    ("calcium", "🦴"),
    ("iron", "⚙️"),
    ("potassium", "🍌"),
]


def _nutri_emoji(label: str) -> str:
    ll = label.lower()
    for key, emoji in NUTRI_EMOJI_MAP:
        if key in ll:
            return emoji
    return "✦"


RECIPE_CSS = """
@keyframes rvFadeUp   { from{opacity:0;transform:translateY(22px)} to{opacity:1;transform:translateY(0)} }
@keyframes rvSlideIn  { from{opacity:0;transform:translateX(-16px)} to{opacity:1;transform:translateX(0)} }
@keyframes rvStepPop  { from{opacity:0;transform:scale(0.90) translateX(-10px)} to{opacity:1;transform:scale(1) translateX(0)} }
@keyframes rvShimmer  { 0%{background-position:-300% center} 100%{background-position:300% center} }
@keyframes rvPulse    { 0%,100%{border-color:rgba(196,148,68,0.28);box-shadow:0 0 0 rgba(196,148,68,0)} 50%{border-color:rgba(196,148,68,0.55);box-shadow:0 0 22px rgba(196,148,68,0.08)} }
@keyframes rvCheckPop { 0%{transform:scale(0)} 60%{transform:scale(1.3)} 100%{transform:scale(1)} }
@keyframes rvNumGlow  { 0%,100%{text-shadow:none} 50%{text-shadow:0 0 18px rgba(196,148,68,0.55)} }
@keyframes rvScanLine { 0%{left:-30%;opacity:0} 10%{opacity:0.7} 90%{opacity:0.7} 100%{left:120%;opacity:0} }
@keyframes crownPulse { 0%,100%{text-shadow:0 0 8px rgba(196,148,68,0.4)} 50%{text-shadow:0 0 22px rgba(196,148,68,0.8), 0 0 40px rgba(196,148,68,0.3)} }
@keyframes ambientPulse { 0%,100%{opacity:0.55} 50%{opacity:0.85} }

body { background:#0A0806; margin:0; padding:1.5rem; }

.rv-root { font-family:'Cormorant Garamond',serif; color:#C8B898; animation:rvFadeUp 0.6s ease-out; padding:0 0 0.5rem; max-width:760px; margin:0 auto; }

.rv-header { text-align:center; padding:2.2rem 1rem 1.8rem; position:relative; overflow:hidden; }
.rv-header::before { content:''; position:absolute; top:0; left:50%; transform:translateX(-50%); width:160px; height:2px; background:linear-gradient(90deg,transparent,#C49444,transparent); }
.rv-chef-emoji { font-size:3rem; display:block; margin-bottom:0.5rem; filter:drop-shadow(0 0 12px rgba(196,148,68,0.55)); animation:crownPulse 3s ease-in-out infinite; }
.rv-title { font-family:'Playfair Display',serif; font-size:clamp(1.7rem,4.5vw,2.6rem); font-weight:800; color:transparent; background:linear-gradient(120deg,#8A6428 0%,#C49444 25%,#EAC870 48%,#D4A850 65%,#A87830 85%,#D4A850 100%); background-size:280% 100%; -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; animation:rvShimmer 5s linear infinite; margin:0 0 0.6rem; letter-spacing:2px; line-height:1.15; }
.rv-eyebrow { font-family:'DM Sans',sans-serif; font-size:0.58rem; letter-spacing:5px; text-transform:uppercase; color:rgba(196,148,68,0.60); margin-bottom:0.4rem; }
.rv-header-bar { width:100px; height:1.5px; background:linear-gradient(90deg,transparent,#C49444,transparent); margin:0.8rem auto 0; animation:ambientPulse 3s ease-in-out infinite; }

.rv-card { background:linear-gradient(145deg,rgba(20,16,10,0.96),rgba(12,9,5,0.98)); border:1px solid rgba(196,148,68,0.22); border-radius:5px; padding:1.5rem 1.8rem; margin-bottom:0.9rem; position:relative; overflow:hidden; animation:rvFadeUp 0.55s ease-out backwards, rvPulse 5s ease-in-out infinite; }
.rv-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1.5px; background:linear-gradient(90deg,transparent,rgba(196,148,68,0.60),transparent); }
.rv-card::after { content:''; position:absolute; top:0; left:-30%; width:25%; height:100%; background:linear-gradient(90deg,transparent,rgba(196,148,68,0.05),transparent); transform:skewX(-18deg); animation:rvScanLine 6s ease-in-out infinite; }
.rv-section-lbl { font-family:'DM Sans',sans-serif; font-size:0.60rem; letter-spacing:4px; text-transform:uppercase; color:#C49444; margin-bottom:1rem; display:flex; align-items:center; gap:10px; }
.rv-section-lbl::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(196,148,68,0.30),transparent); }

.rv-desc { font-family:'Cormorant Garamond',serif; font-size:1.08rem; font-style:italic; color:#C8B898; line-height:1.90; }

.rv-stats { display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:0.9rem; animation:rvFadeUp 0.55s ease-out 0.18s backwards; }
.rv-stat { flex:1; min-width:88px; background:linear-gradient(145deg,rgba(20,16,10,0.96),rgba(12,9,5,0.98)); border:1px solid rgba(196,148,68,0.20); border-radius:5px; padding:1rem 0.8rem; text-align:center; position:relative; overflow:hidden; animation:rvFadeUp 0.55s ease-out backwards, rvPulse 5s ease-in-out infinite; }
.rv-stat::before { content:''; position:absolute; top:0; left:0; right:0; height:1.5px; background:linear-gradient(90deg,transparent,rgba(196,148,68,0.45),transparent); }
.rv-stat-icon { font-size:1.5rem; margin-bottom:0.25rem; }
.rv-stat-val { font-family:'Playfair Display',serif; font-size:0.95rem; font-weight:700; color:#D4A850; margin-bottom:0.15rem; letter-spacing:0.5px; }
.rv-stat-lbl { font-family:'DM Sans',sans-serif; font-size:0.56rem; letter-spacing:2.5px; text-transform:uppercase; color:#8A7A62; }

.rv-ing { display:flex; align-items:center; gap:0.85rem; padding:0.55rem 0.5rem; border-radius:3px; cursor:pointer; transition:background 0.20s ease; animation:rvSlideIn 0.40s ease-out backwards; }
.rv-ing:hover { background:rgba(196,148,68,0.07); }
.rv-chk { display:none; }
.rv-chkbox { width:20px; height:20px; border:1.5px solid rgba(196,148,68,0.38); border-radius:3px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transition:all 0.22s ease; background:rgba(10,8,5,0.80); position:relative; }
.rv-chk:checked + .rv-chkbox { background:#C49444; border-color:#EAC870; animation:rvCheckPop 0.28s ease-out; }
.rv-chk:checked + .rv-chkbox::after { content:'✓'; color:#0A0806; font-size:0.72rem; font-weight:900; position:absolute; font-family:'DM Sans',sans-serif; }
.rv-ing-txt { font-family:'Cormorant Garamond',serif; font-size:1.05rem; color:#C8B898; transition:all 0.22s ease; line-height:1.5; }
.rv-chk:checked + .rv-chkbox + .rv-ing-txt { color:#3E3228; text-decoration:line-through; text-decoration-color:rgba(196,148,68,0.40); }
.rv-ing-sep { height:1px; background:linear-gradient(90deg,rgba(196,148,68,0.08),rgba(196,148,68,0.04),rgba(196,148,68,0.08)); margin:0.1rem 0; }
.rv-ing-hint { font-family:'DM Sans',sans-serif; font-size:0.58rem; letter-spacing:2px; color:rgba(196,148,68,0.40); text-transform:uppercase; margin-bottom:0.8rem; display:flex; align-items:center; gap:6px; }

.rv-step { display:flex; gap:1.1rem; align-items:flex-start; padding:0.95rem 0; border-bottom:1px solid rgba(196,148,68,0.08); animation:rvStepPop 0.45s ease-out backwards; transition:background 0.20s ease; border-radius:3px; padding-left:0.4rem; }
.rv-step:last-child { border-bottom:none; padding-bottom:0; }
.rv-step:hover { background:rgba(196,148,68,0.04); }
.rv-step-num { font-family:'Playfair Display',serif; font-size:1.7rem; font-weight:800; color:transparent; background:linear-gradient(135deg,#8A6428,#C49444,#EAC870); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; min-width:38px; line-height:1; margin-top:0.1rem; flex-shrink:0; animation:rvNumGlow 3.5s ease-in-out infinite; }
.rv-step-txt { font-family:'Cormorant Garamond',serif; font-size:1.05rem; color:#C8B898; line-height:1.90; flex:1; padding-top:0.05rem; }

.rv-tips-grid { display:flex; flex-direction:column; gap:0.7rem; }
.rv-tip { background:linear-gradient(135deg,rgba(42,112,80,0.13),rgba(42,112,80,0.06)); border:1px solid rgba(42,112,80,0.30); border-radius:4px; padding:1rem 1.2rem; display:flex; gap:0.9rem; align-items:flex-start; font-family:'Cormorant Garamond',serif; font-size:1.05rem; color:#C8B898; line-height:1.75; position:relative; overflow:hidden; animation:rvFadeUp 0.50s ease-out backwards; }
.rv-tip::before { content:''; position:absolute; top:0; left:0; right:0; height:1.5px; background:linear-gradient(90deg,transparent,rgba(42,112,80,0.55),transparent); }
.rv-tip-icon { color:#2A7050; font-size:0.82rem; margin-top:0.22rem; flex-shrink:0; }

.rv-plating { background:linear-gradient(135deg,rgba(196,148,68,0.10),rgba(196,148,68,0.03)); border:1px solid rgba(196,148,68,0.28); border-radius:4px; padding:1rem 1.2rem; font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-style:italic; color:#C8B898; line-height:1.85; display:flex; gap:0.9rem; align-items:flex-start; }
.rv-plating-icon { color:#C49444; font-size:0.95rem; margin-top:0.2rem; flex-shrink:0; }

.rv-nutri-grid { display:flex; gap:0.75rem; flex-wrap:wrap; }
.rv-nutri { flex:1; min-width:84px; background:linear-gradient(145deg,rgba(20,16,10,0.96),rgba(12,9,5,0.98)); border:1px solid rgba(196,148,68,0.20); border-radius:5px; padding:0.9rem 0.7rem; text-align:center; position:relative; overflow:hidden; animation:rvFadeUp 0.55s ease-out backwards, rvPulse 5s ease-in-out infinite; }
.rv-nutri::before { content:''; position:absolute; top:0; left:0; right:0; height:1.5px; background:linear-gradient(90deg,transparent,rgba(196,148,68,0.45),transparent); }
.rv-nutri-icon { font-size:1.4rem; margin-bottom:0.25rem; }
.rv-nutri-val { font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:700; color:#D4A850; margin-bottom:0.15rem; }
.rv-nutri-lbl { font-family:'DM Sans',sans-serif; font-size:0.56rem; letter-spacing:2.5px; text-transform:uppercase; color:#8A7A62; }
.rv-nutri-note { font-family:'DM Sans',sans-serif; font-size:0.62rem; letter-spacing:1px; color:rgba(196,148,68,0.45); margin-top:0.7rem; text-align:center; font-style:italic; }

.rv-footer { text-align:center; padding:1.4rem 0 0; color:rgba(196,148,68,0.30); font-family:'DM Sans',sans-serif; font-size:0.58rem; letter-spacing:6px; text-transform:uppercase; animation:rvFadeUp 0.5s ease-out 0.6s backwards; }
"""


def render_recipe(recipe_text: str) -> str:
    """Return fully styled, animated HTML for the recipe."""
    s   = _parse_recipe(recipe_text)
    esc = html_mod.escape

    name     = esc(s.get("Recipe Name", "Your Recipe").strip("[]").strip())
    desc     = esc(s.get("Description", "").strip("[]").strip())
    times    = _parse_times(s.get("Cooking Time", ""))
    serves   = esc(s.get("Serves", "").strip("[]").strip())
    ings     = _list_items(s.get("Ingredients", ""))
    steps    = _list_items(s.get("Instructions", ""))
    tips     = _list_items(s.get("Chef's Tips", ""))
    plating  = esc(s.get("Plating", "").strip("[]").strip())
    nutrition_raw = s.get("Nutrition Estimate", "").strip()

    stat_defs = [("prep","⏱","Prep"),("cook","🔥","Cook"),("total","⌛","Total")]
    stats_html = ""
    for i, (key, icon, label) in enumerate(stat_defs):
        if times.get(key):
            stats_html += f'<div class="rv-stat" style="animation-delay:{i*0.08}s"><div class="rv-stat-icon">{icon}</div><div class="rv-stat-val">{esc(times[key])}</div><div class="rv-stat-lbl">{label}</div></div>'
    if serves:
        stats_html += f'<div class="rv-stat" style="animation-delay:0.24s"><div class="rv-stat-icon">🍽</div><div class="rv-stat-val">{serves}</div><div class="rv-stat-lbl">Serves</div></div>'

    ing_rows = ""
    for i, item in enumerate(ings):
        ing_rows += f'<label class="rv-ing" style="animation-delay:{i*0.035}s"><input type="checkbox" class="rv-chk"/><span class="rv-chkbox"></span><span class="rv-ing-txt">{esc(item)}</span></label>'
        if i < len(ings) - 1:
            ing_rows += '<div class="rv-ing-sep"></div>'

    step_rows = ""
    for i, step in enumerate(steps):
        step_rows += f'<div class="rv-step" style="animation-delay:{i*0.055}s"><div class="rv-step-num">{str(i+1).zfill(2)}</div><div class="rv-step-txt">{esc(step)}</div></div>'

    tip_rows = ""
    for i, tip in enumerate(tips):
        tip_rows += f'<div class="rv-tip" style="animation-delay:{i*0.10}s"><span class="rv-tip-icon">✦</span><span>{esc(tip)}</span></div>'

    plating_html = ""
    if plating:
        plating_html = f'<div class="rv-card" style="animation-delay:0.58s"><div class="rv-section-lbl">✦ &nbsp; Plating</div><div class="rv-plating"><span class="rv-plating-icon">✦</span><span>{plating}</span></div></div>'

    nutrition_html = ""
    if nutrition_raw:
        nutri_items = _list_items(nutrition_raw)
        nutri_cells = ""
        for i, item in enumerate(nutri_items):
            m = re.match(r"^(.*?):\s*(.+)$", item)
            if m:
                label = m.group(1).strip(); value = m.group(2).strip()
            else:
                label = ""; value = item
            icon = _nutri_emoji(label)
            nutri_cells += (
                f'<div class="rv-nutri" style="animation-delay:{i*0.06}s">'
                f'<div class="rv-nutri-icon">{icon}</div>'
                f'<div class="rv-nutri-val">{esc(value)}</div>'
                f'<div class="rv-nutri-lbl">{esc(label)}</div>'
                f'</div>'
            )
        if nutri_cells:
            nutrition_html = f'<div class="rv-card" style="animation-delay:0.70s"><div class="rv-section-lbl">✦ &nbsp; Nutrition Estimate</div><div class="rv-nutri-grid">{nutri_cells}</div><div class="rv-nutri-note">Approximate values per serving — for guidance only</div></div>'

    return f"""
<style>
{RECIPE_CSS}
</style>
<div class="rv-root">
  <div class="rv-header">
    <span class="rv-chef-emoji">👨‍🍳</span>
    <div class="rv-eyebrow">✦ &nbsp; Chef AI Creation &nbsp; ✦</div>
    <div class="rv-title">{name}</div>
    <div class="rv-header-bar"></div>
  </div>
  <div class="rv-card" style="animation-delay:0.08s">
    <div class="rv-section-lbl">✦ &nbsp; The Dish</div>
    <p class="rv-desc">{desc}</p>
  </div>
  <div class="rv-stats">{stats_html}</div>
  <div class="rv-card" style="animation-delay:0.22s">
    <div class="rv-section-lbl">✦ &nbsp; Ingredients</div>
    <div class="rv-ing-hint">✦ &nbsp; tap to check off as you cook</div>
    <div>{ing_rows}</div>
  </div>
  <div class="rv-card" style="animation-delay:0.34s">
    <div class="rv-section-lbl">✦ &nbsp; Method</div>
    <div>{step_rows}</div>
  </div>
  <div class="rv-card" style="animation-delay:0.46s">
    <div class="rv-section-lbl">✦ &nbsp; Chef's Tips</div>
    <div class="rv-tips-grid">{tip_rows}</div>
  </div>
{plating_html}{nutrition_html}
  <div class="rv-footer">✦ ─── ✦ ─── ✦ &nbsp; Chef AI &nbsp; ✦ ─── ✦ ─── ✦</div>
</div>
"""


def build_html_export(recipe_text: str) -> str:
    name = _parse_recipe(recipe_text).get("Recipe Name", "Chef AI Recipe").strip("[]").strip()
    body = render_recipe(recipe_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{html_mod.escape(name)} — Chef AI</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,800;1,400&family=DM+Sans:ital,wght@0,400;0,500;0,600&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>* {{ box-sizing:border-box; }}</style>
</head>
<body>
{body}
</body>
</html>"""


# ════════════════════════════════════════════
#  LOADING SKELETON
# ════════════════════════════════════════════
def loading_skeleton_html() -> str:
    ing_rows  = "".join('<div class="skel-block skel-row"></div>' for _ in range(4))
    step_rows = "".join('<div class="skel-block skel-row" style="height:64px;"></div>' for _ in range(3))
    return f"""
<div class="skel-root">
  <div class="skel-eyebrow">✦ &nbsp; Your AI chef is crafting the perfect recipe &nbsp; ✦</div>
  <div class="skel-block skel-title"></div>
  <div class="skel-block skel-card" style="margin-bottom:1.2rem;"></div>
  <div style="display:flex;gap:0.75rem;margin-bottom:0.9rem;">
    <div class="skel-block" style="flex:1;height:78px;"></div>
    <div class="skel-block" style="flex:1;height:78px;"></div>
    <div class="skel-block" style="flex:1;height:78px;"></div>
  </div>
  <div class="skel-block" style="height:18px;width:40%;margin-bottom:0.8rem;"></div>
  {ing_rows}
  <div class="skel-block" style="height:18px;width:30%;margin:1.2rem 0 0.8rem;"></div>
  {step_rows}
</div>
"""


# ════════════════════════════════════════════
#  RECIPE HISTORY SIDEBAR
# ════════════════════════════════════════════
def render_history_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="hist-header">
            <span class="hist-header-icon">📜</span>
            <span class="hist-header-text">Recipe History</span>
            <span class="hist-header-count">{len(st.session_state.recipe_history)}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.current_recipe is not None or st.session_state.view_recipe_id is not None:
            st.markdown('<div class="hist-new-wrap">', unsafe_allow_html=True)
            if st.button("✦  Start New Recipe", key="hist_new_recipe", use_container_width=True):
                st.session_state.current_recipe = None
                st.session_state.current_recipe_name = None
                st.session_state.view_recipe_id = None
                st.session_state.chat_history = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if not st.session_state.recipe_history:
            st.markdown("""
            <div class="hist-empty">
                <span class="hist-empty-icon">🍳</span>
                No recipes yet.<br/>Craft your first dish<br/>and it will appear here.
            </div>
            """, unsafe_allow_html=True)
            return

        for entry in reversed(st.session_state.recipe_history):
            is_active = (st.session_state.view_recipe_id == entry["id"]) or \
                        (st.session_state.current_recipe_name == entry["name"] and
                         st.session_state.view_recipe_id is None and
                         entry == st.session_state.recipe_history[-1])
            active_class = "active" if is_active else ""

            meta_chips = ""
            if entry.get("cuisine") and entry["cuisine"] != "Any":
                meta_chips += f'<span>🌍 {html_mod.escape(entry["cuisine"])}</span>'
            if entry.get("meal_type") and entry["meal_type"] != "Any":
                meta_chips += f'<span>🍽 {html_mod.escape(entry["meal_type"])}</span>'
            if entry.get("diet") and entry["diet"] != "None":
                meta_chips += f'<span>🥗 {html_mod.escape(entry["diet"])}</span>'

            ing_preview = html_mod.escape(entry.get("ingredients", "")[:120])
            if len(entry.get("ingredients", "")) > 120:
                ing_preview += "…"

            st.markdown(f"""
            <div class="hist-card {active_class}">
                <div class="hist-card-top">
                    <div class="hist-card-name">{html_mod.escape(entry['name'])}</div>
                    <div class="hist-card-badge">#{entry['id']}</div>
                </div>
                <div class="hist-card-meta">{meta_chips}</div>
                <div class="hist-card-time">🕐 {html_mod.escape(entry['time'])}</div>
                <div class="hist-card-ing">✦ {ing_preview}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="hist-card-actions">', unsafe_allow_html=True)
            if st.button("👁  View Recipe", key=f"view_{entry['id']}", use_container_width=True):
                st.session_state.view_recipe_id = entry["id"]
                st.session_state.current_recipe = entry["raw"]
                st.session_state.current_recipe_name = entry["name"]
                st.session_state.chat_history = entry.get("chat_history", [])
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hist-clear-wrap">', unsafe_allow_html=True)
        if st.button("🗑  Clear All History", key="hist_clear_all", use_container_width=True):
            st.session_state.recipe_history = []
            st.session_state.current_recipe = None
            st.session_state.current_recipe_name = None
            st.session_state.view_recipe_id = None
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hist-footer">✦ Chef AI ✦</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  ROUTING
# ════════════════════════════════════════════════════════════
page = st.session_state.page

# ─────────────────────────────────────────────
#  SPLASH PAGE
# ─────────────────────────────────────────────
if page == "splash":
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display:none !important; }
        [data-testid="stSidebarCollapsedControl"] { display:none !important; }
        [data-testid="stSidebarCollapseButton"]   { display:none !important; }
        .main .block-container { max-width:100% !important; padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sp-hud tl"></div><div class="sp-hud tr"></div>
    <div class="sp-hud bl"></div><div class="sp-hud br"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="splash-root">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sp-robot-wrap">
        <div class="sp-robot-ring sp-ring-outer"></div>
        <div class="sp-robot-ring sp-ring-mid"></div>
        <div class="sp-robot-ring sp-ring-inner"></div>
        <img src="data:image/svg+xml;base64,{_robot_b64}" width="120" height="174"
             alt="Robot Chef"
             style="position:relative;z-index:2;filter:drop-shadow(0 0 18px rgba(196,148,68,0.45)) drop-shadow(0 8px 28px rgba(0,0,0,0.85));"/>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sp-badge-wrap">
        <div class="sp-badge-inner">
            <div class="sp-title-eyebrow">✦ &nbsp; AI Culinary Intelligence &nbsp; ✦</div>
            <div class="sp-title-main">CHEF&nbsp;AI</div>
            <div class="sp-title-sub">Your personal Michelin-star kitchen companion</div>
            <div class="sp-badge-bar"></div>
            <p class="sp-badge-desc">
                Tell the AI what's in your fridge. Pick a cuisine, a mood, a constraint —
                and watch it craft a <strong>restaurant-quality recipe</strong> in seconds.
                From street food to haute cuisine, every dish deserves a great recipe.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sp-version-chip">
        <span class="sp-version-dot"></span>
        v2.2 &nbsp;·&nbsp; Groq LLaMA 3.3 70B &nbsp;·&nbsp; Online
        <span class="sp-version-dot"></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sp-cta-hint">▾ &nbsp; click to begin &nbsp; ▾</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.1, 1.8, 1.1])
    with col2:
        if st.button("🍽️  Enter the Kitchen", type="primary", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()

    st.markdown(f"""
    <div style="display:flex;justify-content:center;margin:1.6rem 0 0.5rem;">
        <div class="sp-creator-wrap">
            <div class="sp-creator-card">
                <div class="sp-avatar-shell">
                    <div class="sp-avatar">AR</div>
                </div>
                <div>
                    <div class="sp-creator-name">Abdul Rehman Raja</div>
                    <div class="sp-creator-role">BSCS · FAST-NUCES Islamabad</div>
                    <div class="sp-tags">
                        <span class="sp-tag sp-tag-amber">Groq API</span>
                        <span class="sp-tag sp-tag-green">LLaMA 3.3 70B</span>
                        <span class="sp-tag sp-tag-cream">Streamlit</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center;font-family:'DM Sans',sans-serif;font-size:0.6rem;
    color:rgba(62,50,40,0.60);letter-spacing:2.5px;margin-top:0.6rem;text-transform:uppercase;">
    Chef AI &nbsp;·&nbsp; FAST-NUCES 2025 &nbsp;·&nbsp; Abdul Rehman Raja
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN PAGE
# ─────────────────────────────────────────────
elif page == "main":

    render_history_sidebar()

    st.markdown(f"""
    <div class="main-hero" style="animation:fadeIn 0.7s ease-out;">
        <img src="data:image/svg+xml;base64,{_robot_b64}" width="110" height="160"
             alt="Chef AI Robot"
             style="margin-bottom:0.6rem;
                    filter:drop-shadow(0 0 14px rgba(196,148,68,0.40)) drop-shadow(0 6px 20px rgba(0,0,0,0.80));
                    animation:robotBob 4s ease-in-out infinite;"/>
        <div class="main-rule">
            <div class="main-rule-line"></div>
            <span class="main-rule-icon">✦</span>
            <div class="main-rule-line r"></div>
        </div>
        <h1 class="main-title">CHEF AI</h1>
        <div class="main-rule">
            <div class="main-rule-line"></div>
            <span class="main-rule-icon">✦</span>
            <div class="main-rule-line r"></div>
        </div>
        <p class="main-tagline">Turn your ingredients into restaurant-quality recipes — instantly.</p>
        <p class="main-credit">✦ Created by Abdul Rehman Raja</p>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  RECIPE DISPLAY VIEW
    # ─────────────────────────────────────────
    if st.session_state.current_recipe is not None:

        recipe      = st.session_state.current_recipe
        recipe_name = st.session_state.current_recipe_name or \
                      _parse_recipe(recipe).get("Recipe Name", "Your Recipe").strip("[]").strip()

        st.success("✦  Your recipe is ready — Bon appétit!")
        st.markdown(render_recipe(recipe), unsafe_allow_html=True)

        st.divider()

        # ── Refine / follow-up ──
        st.markdown('<div class="section-card" style="animation-delay:0.05s;">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">✦ &nbsp; Refine This Recipe</div>', unsafe_allow_html=True)
        followup = st.text_area(
            label="followup_input", label_visibility="collapsed",
            placeholder="e.g.  Make it spicier · Use less oil · Swap chicken for paneer · Make it for 6 people ...",
            height=85, key="followup_text"
        )
        refine_clicked = st.button("✦  Refine Recipe", use_container_width=True, key="refine_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if refine_clicked:
            if not followup.strip():
                st.warning("Please describe how you'd like to adjust the recipe.")
            else:
                placeholder = st.empty()
                placeholder.markdown(loading_skeleton_html(), unsafe_allow_html=True)

                system_msg = {
                    "role": "system",
                    "content": (
                        "You are a world-class chef with 20 years of culinary experience. "
                        "You create precise, delicious, beautifully written recipes. "
                        "Always follow the exact format requested. Never add preambles or apologies. "
                        "The user may ask you to adjust a previously generated recipe — "
                        "apply their requested change while keeping the same output format."
                    )
                }
                if not st.session_state.chat_history:
                    st.session_state.chat_history = [{"role": "assistant", "content": recipe}]

                user_msg = {
                    "role": "user",
                    "content": (
                        f"Please adjust the previous recipe as follows: {followup.strip()}. "
                        "Re-output the FULL recipe again using the exact same '## ' section headings format "
                        "(Recipe Name, Description, Ingredients, Instructions, Cooking Time, Serves, "
                        "Chef's Tips, Plating, Nutrition Estimate)."
                    )
                }
                messages = [system_msg] + st.session_state.chat_history + [user_msg]

                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages, max_tokens=1600, temperature=0.85
                    )
                    new_recipe = response.choices[0].message.content
                    placeholder.empty()

                    st.session_state.chat_history.append({"role": "user",      "content": user_msg["content"]})
                    st.session_state.chat_history.append({"role": "assistant", "content": new_recipe})

                    new_name = _parse_recipe(new_recipe).get("Recipe Name", recipe_name).strip("[]").strip()
                    st.session_state.current_recipe      = new_recipe
                    st.session_state.current_recipe_name = new_name

                    if st.session_state.view_recipe_id is not None:
                        for entry in st.session_state.recipe_history:
                            if entry["id"] == st.session_state.view_recipe_id:
                                entry["raw"]          = new_recipe
                                entry["name"]         = new_name
                                entry["chat_history"] = st.session_state.chat_history
                                break
                    st.rerun()

                except AuthenticationError:
                    placeholder.empty()
                    st.error("Invalid API key. Please check your GROQ_API_KEY in the .env file.")
                except RateLimitError:
                    placeholder.empty()
                    st.warning("Rate limit hit — please wait a moment and try again.")
                except APIConnectionError:
                    placeholder.empty()
                    st.error("Couldn't connect to the AI service. Please check your internet connection.")
                except Exception as e:
                    placeholder.empty()
                    st.error(f"Unexpected error: {e}")

        st.divider()

        # ── Download / actions ──
        st.markdown('<div class="recipe-action-row">', unsafe_allow_html=True)
        dl_col1, dl_col2, share_col = st.columns([1.4, 1.4, 1])
        with dl_col1:
            st.download_button(
                label="⬇  Download (.txt)", data=recipe,
                file_name=f"{re.sub(r'[^a-zA-Z0-9_-]+','_',recipe_name) or 'chef_ai_recipe'}.txt",
                mime="text/plain", use_container_width=True
            )
        with dl_col2:
            html_export = build_html_export(recipe)
            st.download_button(
                label="⬇  Download (.html)", data=html_export,
                file_name=f"{re.sub(r'[^a-zA-Z0-9_-]+','_',recipe_name) or 'chef_ai_recipe'}.html",
                mime="text/html", use_container_width=True
            )
        with share_col:
            if st.button("⟳  New Recipe", use_container_width=True, key="new_recipe_btn"):
                st.session_state.current_recipe      = None
                st.session_state.current_recipe_name = None
                st.session_state.view_recipe_id      = None
                st.session_state.chat_history        = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────
    #  GENERATION FORM
    # ─────────────────────────────────────────
    else:
        st.markdown('<div class="section-card" style="animation-delay:0.1s;">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">✦ &nbsp; Your Ingredients</div>', unsafe_allow_html=True)
        ingredients = st.text_area(
            label="ingredients_input", label_visibility="collapsed",
            placeholder="e.g.  chicken breast, tomatoes, onion, garlic, lemon, fresh herbs ...",
            height=115, key="ingredients"
        )
        if ingredients.strip():
            wc = len(ingredients.split(","))
            st.markdown(
                f'<p style="font-family:DM Sans,sans-serif;font-size:0.65rem;letter-spacing:2px;'
                f'color:rgba(196,148,68,0.55);margin:0.3rem 0 0;text-transform:uppercase;">'
                f'{wc} ingredient{"s" if wc!=1 else ""} detected</p>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="animation-delay:0.2s;">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">⚙ &nbsp; Recipe Preferences</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            cuisine   = st.selectbox("Cuisine Style",       ["Any","Pakistani","Arabic","Chinese","Italian","Indian","Mediterranean","Thai"])
        with col2:
            meal_type = st.selectbox("Meal Type",           ["Any","Breakfast","Lunch","Dinner","Snack","Dessert"])
        with col3:
            diet      = st.selectbox("Dietary Preference",  ["None","Vegetarian","Vegan","Spicy 🌶️","Low Oil","Under 30 min"])
        st.markdown('</div>', unsafe_allow_html=True)

        generate = st.button("✦  Craft My Recipe", use_container_width=True)

        if generate:
            valid, err_msg = validate_ingredients(ingredients)
            if not valid:
                st.warning(err_msg)
            else:
                placeholder = st.empty()
                placeholder.markdown(loading_skeleton_html(), unsafe_allow_html=True)

                cuisine_text = f"The cuisine style must be {cuisine}." if cuisine != "Any" else ""
                meal_text    = f"This is for {meal_type}."             if meal_type != "Any" else ""
                diet_text    = f"Dietary requirement: {diet}."         if diet != "None" else ""
                cuisine_note = CUISINE_NOTES.get(cuisine, "")

                prompt = f"""You are a world-class professional chef. A user has these ingredients: {ingredients}.
{cuisine_text} {meal_text} {diet_text}
{cuisine_note}

Create a detailed, mouth-watering recipe using mainly these ingredients.
Assume the user has basic pantry items: salt, black pepper, oil, water, and common spices.

Format your response EXACTLY using these markdown headings — no extra commentary outside them:

## Recipe Name
[A creative, appetising name for the dish]

## Description
[2 sentences — what makes this dish special and when to serve it]

## Ingredients
[Numbered list with exact quantities, e.g. "1. 300g boneless chicken, cubed"]

## Instructions
[Numbered steps — clear, precise, with temperatures and timings where relevant]

## Cooking Time
- Prep: [X min]
- Cook: [X min]
- Total: [X min]

## Serves
[Number of people]

## Chef's Tips
[2 professional tips that elevate this dish]

## Plating
[One line describing how to present this dish beautifully]

## Nutrition Estimate
[Approximate per-serving values as a list, e.g. "Calories: 450 kcal", "Protein: 32g", "Carbs: 40g", "Fat: 18g"]

Write confidently. Use specific quantities. Make it genuinely delicious.
"""

                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are a world-class chef with 20 years of culinary experience. You create precise, delicious, beautifully written recipes. Always follow the exact format requested. Never add preambles or apologies."},
                            {"role": "user",   "content": prompt}
                        ],
                        max_tokens=1600, temperature=0.85
                    )

                    recipe      = response.choices[0].message.content
                    recipe_name = _parse_recipe(recipe).get("Recipe Name", "Your Recipe").strip("[]").strip()
                    placeholder.empty()

                    new_id = len(st.session_state.recipe_history) + 1
                    history_entry = {
                        "id": new_id,
                        "name": recipe_name,
                        "time": datetime.datetime.now().strftime("%b %d, %Y · %I:%M %p"),
                        "raw": recipe,
                        "ingredients": ingredients.strip(),
                        "cuisine": cuisine,
                        "meal_type": meal_type,
                        "diet": diet,
                        "chat_history": [{"role": "assistant", "content": recipe}],
                    }
                    st.session_state.recipe_history.append(history_entry)

                    st.session_state.current_recipe      = recipe
                    st.session_state.current_recipe_name = recipe_name
                    st.session_state.view_recipe_id      = new_id
                    st.session_state.chat_history        = history_entry["chat_history"]

                    st.rerun()

                except AuthenticationError:
                    placeholder.empty()
                    st.error("Invalid API key. Please check your GROQ_API_KEY in the .env file.")
                    st.info("Double-check that your GROQ_API_KEY in .env is correct and active.")
                except RateLimitError:
                    placeholder.empty()
                    st.warning("Rate limit hit — please wait a moment and try again.")
                except APIConnectionError:
                    placeholder.empty()
                    st.error("Couldn't connect to the AI service. Please check your internet connection.")
                except Exception as e:
                    placeholder.empty()
                    st.error(f"Unexpected error: {e}")
                    st.info("Double-check that your GROQ_API_KEY in .env is correct and active.")

        if not generate:
            st.markdown("""
            <div class="empty-hint">
                ✦ &nbsp; Try: chicken · garlic · lemon &nbsp;→&nbsp; Pakistani &nbsp;→&nbsp; Craft My Recipe
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-wrap">
        <div class="footer-ornament">✦ ─── ✦ ─── ✦</div>
        <div class="footer-main">Chef AI</div>
        <div class="footer-sub">Crafted by Abdul Rehman Raja &nbsp;·&nbsp; Streamlit + Groq AI · LLaMA 3.3 70B</div>
    </div>
    """, unsafe_allow_html=True)
