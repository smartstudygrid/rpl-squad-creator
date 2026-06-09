import streamlit as st
from supabase import create_client, Client
import base64
import io
from PIL import Image

# --- 1. DATABASE CONNECTION ---
try:
    url = "https://blhxvguboircijscdhhn.supabase.co"
    key = "sb_publishable_3Q3wcRqlLi86GrlygGeEaA_UjWlp66L"
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Challenger's Cup", layout="wide")

# --- 3. CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Oswald:wght@400;600;700&display=swap');

    /* ===== GLOBAL BACKGROUND ===== */
    .stApp {
        background: 
            radial-gradient(ellipse at 50% 100%, rgba(0,80,180,0.25) 0%, transparent 60%),
            radial-gradient(ellipse at 20% 50%, rgba(0,40,120,0.2) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 50%, rgba(0,40,120,0.2) 0%, transparent 50%),
            linear-gradient(180deg, #020818 0%, #040d2a 40%, #061535 70%, #03100d 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    /* Stadium lights effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 15% 0%, rgba(100,160,255,0.12) 0%, transparent 40%),
            radial-gradient(ellipse at 85% 0%, rgba(100,160,255,0.12) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem !important; }

    /* ===== LEAGUE HEADER ===== */
    .league-header {
        text-align: center;
        padding: 18px 0 8px 0;
        position: relative;
    }
    .league-title {
        font-family: 'Oswald', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: #7ab3ff;
        margin-bottom: 4px;
    }
    .league-name {
        font-family: 'Oswald', sans-serif;
        font-size: 48px;
        font-weight: 700;
        text-transform: uppercase;
        background: linear-gradient(135deg, #c8a84b 0%, #f5d073 35%, #ffeea0 50%, #f5d073 65%, #c8a84b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        text-shadow: none;
        filter: drop-shadow(0 0 20px rgba(200,168,75,0.5));
    }
    .league-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 13px;
        letter-spacing: 3px;
        color: rgba(200,200,220,0.6);
        margin-top: 4px;
    }
    .league-divider {
        width: 300px;
        height: 1px;
        background: linear-gradient(90deg, transparent, #c8a84b, transparent);
        margin: 10px auto 0 auto;
    }

    /* ===== LOGIN PAGE ===== */
    .login-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 36px 32px;
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(200,168,75,0.3);
        border-radius: 12px;
        box-shadow: 0 0 60px rgba(0,80,200,0.15), inset 0 1px 0 rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }
    .login-title {
        font-family: 'Oswald', sans-serif;
        font-size: 22px;
        font-weight: 600;
        color: #f5d073;
        text-align: center;
        letter-spacing: 3px;
        margin-bottom: 24px;
        text-transform: uppercase;
    }

    /* ===== STREAMLIT WIDGET OVERRIDES ===== */
    .stTextInput label p, .stSelectbox label p {
        font-family: 'Rajdhani', sans-serif !important;
        color: rgba(200,210,255,0.7) !important;
        font-size: 12px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
    }
    .stTextInput input, .stSelectbox > div > div {
        background: rgba(0,20,60,0.6) !important;
        border: 1px solid rgba(100,150,255,0.2) !important;
        color: white !important;
        border-radius: 6px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 15px !important;
    }
    .stTextInput input:focus, .stSelectbox > div > div:focus {
        border-color: rgba(200,168,75,0.6) !important;
        box-shadow: 0 0 12px rgba(200,168,75,0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #c8a84b, #f5d073) !important;
        color: #0a0a1a !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        font-size: 14px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #f5d073, #fff0a0) !important;
        box-shadow: 0 0 20px rgba(245,208,115,0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stToggle label p,
    .stToggle label span,
    .stToggle label div,
    .stToggle > label {
        font-family: 'Rajdhani', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 2px !important;
    }

    /* ===== TEAM HEADER ===== */
    .team-header-wrap {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 12px 0 20px 0;
        border-bottom: 1px solid rgba(200,168,75,0.2);
        margin-bottom: 24px;
    }
    .logo-circle {
        width: 140px; height: 140px;
        border-radius: 50%;
        border: 3px solid #c8a84b;
        overflow: hidden;
        background: rgba(0,20,60,0.8);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(200,168,75,0.3);
        flex-shrink: 0;
    }
    .logo-circle img { width: 100%; height: 100%; object-fit: cover; }
    .logo-placeholder { width: 140px; height: 140px; border-radius: 50%; border: 2px dashed rgba(200,168,75,0.3); background: rgba(0,20,60,0.4); }

    .team-name-display {
        font-family: 'Oswald', sans-serif;
        font-size: 38px;
        font-weight: 700;
        text-transform: uppercase;
        background: linear-gradient(135deg, #c8a84b, #f5d073, #c8a84b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        filter: drop-shadow(0 0 10px rgba(200,168,75,0.3));
    }
    .team-subtitle-tag {
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        letter-spacing: 4px;
        color: rgba(150,180,255,0.6);
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* ===== PLAYER CARD - GLOWING ODI STYLE ===== */
    .player-card-outer {
        position: relative;
        margin: 6px 4px;
        cursor: pointer;
    }

    /* Outer glow ring */
    .player-card-glow {
        position: absolute;
        inset: -3px;
        border-radius: 10px;
        background: linear-gradient(135deg, #1a6fff, #00cfff, #1a6fff, #0044cc);
        opacity: 0.7;
        filter: blur(3px);
        z-index: 0;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { opacity: 0.6; filter: blur(3px); }
        50% { opacity: 1; filter: blur(5px); }
    }

    /* Gold corner accents */
    .player-card-inner {
        position: relative;
        z-index: 1;
        background: linear-gradient(160deg, #0a1628 0%, #060f20 60%, #0a1a10 100%);
        border: 1.5px solid rgba(100,180,255,0.4);
        border-radius: 8px;
        overflow: hidden;
        padding: 0;
    }
    .player-card-inner::before,
    .player-card-inner::after {
        content: '';
        position: absolute;
        width: 14px; height: 14px;
        border-color: #c8a84b;
        border-style: solid;
        z-index: 2;
    }
    .player-card-inner::before { top: 3px; left: 3px; border-width: 2px 0 0 2px; border-radius: 3px 0 0 0; }
    .player-card-inner::after  { bottom: 3px; right: 3px; border-width: 0 2px 2px 0; border-radius: 0 0 3px 0; }

    .card-img-area {
        width: 100%;
        aspect-ratio: 1 / 1;
        overflow: hidden;
        background: linear-gradient(180deg, rgba(10,30,60,0.8) 0%, rgba(5,15,30,0.9) 100%);
        display: flex; align-items: center; justify-content: center;
        position: relative;
    }
    .card-img-area img { width: 100%; height: 100%; object-fit: cover; }

    /* Holographic shimmer overlay */
    .card-img-area::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(100,180,255,0.08) 0%, transparent 50%, rgba(200,168,75,0.05) 100%);
        pointer-events: none;
    }

    /* Empty card icon */
    .card-empty-icon {
        width: 50%;
        height: 50%;
        opacity: 0.15;
        display: flex; align-items: center; justify-content: center;
    }

    .card-name-bar {
        padding: 5px 6px 6px 6px;
        background: linear-gradient(180deg, rgba(0,20,60,0.9), rgba(0,10,30,0.95));
        border-top: 1px solid rgba(100,180,255,0.2);
        text-align: center;
    }
    .card-name-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        font-weight: 700;
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .card-name-empty {
        font-family: 'Rajdhani', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: rgba(100,150,255,0.4);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Number badge */
    .card-num {
        position: absolute;
        top: 5px; left: 6px;
        font-family: 'Oswald', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: rgba(200,168,75,0.7);
        line-height: 1;
        z-index: 3;
    }

    /* ===== CAPTAIN CARD ===== */
    .captain-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0;
    }
    .captain-label {
        font-family: 'Oswald', sans-serif;
        font-size: 11px;
        letter-spacing: 5px;
        color: #c8a84b;
        text-transform: uppercase;
        text-align: center;
        padding: 6px 4px 4px 4px;
        background: linear-gradient(180deg, rgba(0,30,10,0.9), rgba(5,15,5,0.8));
        border-bottom: 1px solid rgba(200,168,75,0.25);
        width: 100%;
    }
    .captain-card-outer {
        position: relative;
        width: 100%;
        max-width: 100%;
    }
    .captain-card-glow {
        position: absolute;
        inset: -5px;
        border-radius: 12px;
        background: linear-gradient(135deg, #c8a84b, #f5d073, #c8a84b, #f5d073);
        opacity: 0.8;
        filter: blur(6px);
        animation: captainGlow 2.5s ease-in-out infinite;
    }
    @keyframes captainGlow {
        0%, 100% { opacity: 0.6; filter: blur(6px); }
        50% { opacity: 1; filter: blur(10px); }
    }
    .captain-card-inner {
        position: relative;
        z-index: 1;
        background: linear-gradient(160deg, #0e1a08 0%, #060f04 60%, #0a1a28 100%);
        border: 2px solid rgba(200,168,75,0.6);
        border-radius: 10px;
        overflow: hidden;
    }
    .captain-card-inner::before,
    .captain-card-inner::after {
        content: '';
        position: absolute;
        width: 18px; height: 18px;
        border-color: #f5d073;
        border-style: solid;
        z-index: 2;
    }
    .captain-card-inner::before { top: 4px; left: 4px; border-width: 2px 0 0 2px; border-radius: 4px 0 0 0; }
    .captain-card-inner::after  { bottom: 4px; right: 4px; border-width: 0 2px 2px 0; border-radius: 0 0 4px 0; }

    .captain-img-area {
        width: 100%;
        min-height: 240px;
        max-height: 340px;
        overflow: hidden;
        background: linear-gradient(180deg, rgba(20,40,10,0.8) 0%, rgba(5,15,5,0.9) 100%);
        display: flex; align-items: center; justify-content: center;
        position: relative;
    }
    .captain-img-area img { width: 100%; height: 100%; object-fit: cover; }

    /* Captain number badge */
    .captain-num {
        position: absolute;
        top: 36px; left: 7px;
        font-family: 'Oswald', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: rgba(200,168,75,0.85);
        line-height: 1;
        z-index: 3;
    }

    /* Captain star badge */
    .captain-star {
        position: absolute;
        top: 6px; right: 7px;
        font-size: 18px;
        z-index: 3;
        filter: drop-shadow(0 0 6px rgba(200,168,75,0.8));
    }

    .captain-name-bar {
        padding: 8px 6px 10px 6px;
        background: linear-gradient(180deg, rgba(0,30,10,0.9), rgba(0,15,5,0.95));
        border-top: 1px solid rgba(200,168,75,0.3);
        text-align: center;
    }
    .captain-name-text {
        font-family: 'Oswald', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #f5d073;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* ===== EDIT MODE INPUTS ===== */
    .stTextInput input { font-size: 13px !important; padding: 4px 8px !important; }

    /* Small upload button */
    .stFileUploader label { display: none !important; }
    .stFileUploader section {
        padding: 2px !important;
        min-height: unset !important;
        border: 1px dashed rgba(200,168,75,0.3) !important;
        background: rgba(0,20,60,0.3) !important;
        border-radius: 4px !important;
    }
    .stFileUploader section > div { display: none !important; }
    .stFileUploader button {
        font-size: 0 !important;
        width: 28px !important; height: 28px !important;
        background: rgba(200,168,75,0.2) !important;
        border-radius: 4px !important;
        border: 1px solid #c8a84b !important;
        margin: 1px auto !important;
    }
    .stFileUploader button::before { content: "⬆"; font-size: 14px; color: #f5d073; }

    /* ===== LOCKED BANNER ===== */
    .locked-banner {
        background: linear-gradient(90deg, rgba(200,168,75,0.1), rgba(200,168,75,0.2), rgba(200,168,75,0.1));
        border: 1px solid rgba(200,168,75,0.4);
        border-radius: 6px;
        padding: 8px 16px;
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        font-size: 13px;
        letter-spacing: 3px;
        color: #c8a84b;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    /* ===== ADMIN SECTION ===== */
    .admin-divider {
        border: none;
        border-top: 1px solid rgba(200,168,75,0.15);
        margin: 20px 0;
    }
    .admin-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        letter-spacing: 3px;
        color: rgba(150,150,180,0.5);
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 12px;
    }

    /* ===== VIEW SQUAD BUTTON (blue outline style) ===== */
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #7ab3ff !important;
        border: 1px solid rgba(100,160,255,0.4) !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 3px !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(100,160,255,0.08) !important;
        border-color: rgba(100,160,255,0.7) !important;
        box-shadow: 0 0 16px rgba(100,160,255,0.2) !important;
    }

    /* ===== VIEW MODE BADGE ===== */
    .view-mode-badge {
        display: inline-block;
        background: linear-gradient(90deg, rgba(100,160,255,0.1), rgba(100,160,255,0.18), rgba(100,160,255,0.1));
        border: 1px solid rgba(100,160,255,0.35);
        border-radius: 6px;
        padding: 7px 14px;
        text-align: center;
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        letter-spacing: 3px;
        color: #7ab3ff;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* ===== FOOTER ===== */
    .rpl-footer {
        position: fixed;
        bottom: 10px; left: 14px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        color: white;
        text-transform: uppercase;
    }
    .rpl-footer a {
        color: white;
        text-decoration: underline;
    }
    .rpl-footer a:hover {
        color: #f5d073;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="league-header">
        <div class="league-title">&#9670; Season 18 2026 &#9670;</div>
        <div class="league-name">Challenger's Cup</div>
        <div class="league-subtitle">Build Your Squad</div>
        
    <div class="rpl-footer"><a href="https://www.smartstudygrid.com" target="_blank">www.smartstudygrid.com</a> &nbsp;|&nbsp; Created by Amanullah Khan &nbsp;|&nbsp; +966568959394</div>
""", unsafe_allow_html=True)

# --- 4. IMAGE PROCESSING ---
def img_to_base64(image_file):
    if image_file is None: return None
    img = Image.open(image_file).convert("RGB")
    img.thumbnail((300, 300))
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- 5. APP STATE ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'team' not in st.session_state: st.session_state.team = None
if 'view_only' not in st.session_state: st.session_state.view_only = False

# =============================================
# --- NAVIGATION: LOGIN SCREEN ---
# =============================================
if st.session_state.page == 'home':
    _, c2, _ = st.columns([1, 1.4, 1])
    with c2:
        
        st.markdown('<div class="login-title">⚡ Enter Your Squad</div>', unsafe_allow_html=True)

        t = st.selectbox("Select Your Team", [
            "Gladiators YB", "KHAN JEE", "KAPTAN 11",
            "Pak EAGLES", "RCC", "SWAT XI",
            "Riyadh Stallions", "Riyadh Strikers", "Saudi German",
            "Punjab XI", "Riyadh Kings", "Team Avengers"
        ])
        p = st.text_input("Password", type="password", placeholder="Enter team password…")

        if st.button("Enter Dashboard", use_container_width=True):
            if p == "myteam123":
                st.session_state.page = 'squad'
                st.session_state.team = t
                st.session_state.view_only = False
                st.rerun()
            else:
                st.error("Incorrect password.")

        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

        if st.button("👁️  View Squad", use_container_width=True, type="secondary"):
            st.session_state.page = 'squad'
            st.session_state.team = t
            st.session_state.view_only = True
            st.rerun()

    
        st.markdown('<div class="admin-label">🔒 League Admin</div>', unsafe_allow_html=True)
        admin_pass = st.text_input("Admin Password", type="password", key="admin_p", placeholder="Admin only…")

        if admin_pass == "Pakistan1947":
            col_lock, col_unlock = st.columns(2)
            if col_lock.button("🔒 Lock All", use_container_width=True):
                supabase.table("squads").update({"is_locked": True}).neq("team_name", "temp").execute()
                st.success("All squads LOCKED.")
            if col_unlock.button("🔓 Unlock All", use_container_width=True):
                supabase.table("squads").update({"is_locked": False}).neq("team_name", "temp").execute()
                st.success("All squads UNLOCKED.")

        st.markdown('</div>', unsafe_allow_html=True)

# =============================================
# --- NAVIGATION: SQUAD SCREEN ---
# =============================================
elif st.session_state.page == 'squad':
    team = st.session_state.team

    res = supabase.table("squads").select("*").eq("team_name", team).execute()

    if not res.data:
        st.error(f"Team '{team}' not found in database.")
        if st.button("Back to Login"):
            st.session_state.page = 'home'
            st.rerun()
        st.stop()

    db_data = res.data[0]
    is_locked = db_data.get('is_locked', False)
    names = db_data.get('player_list', [""] * 17)
    pics = db_data.get('squad_pics', {})
    cap_name = db_data.get('captain_name', "Captain")
    cap_pic = db_data.get('cap_pic', None)
    team_logo = db_data.get('team_logo', None)
    view_only = st.session_state.get('view_only', False)

    # --- TEAM HEADER BAR ---
    if team_logo:
        logo_html = f'<div class="logo-circle"><img src="data:image/jpeg;base64,{team_logo}"></div>'
    else:
        logo_html = '<div class="logo-placeholder"></div>'

    st.markdown(f"""
        <div class="team-header-wrap">
            {logo_html}
            <div>
                <div class="team-name-display">{team}</div>
                <div class="team-subtitle-tag">Challenger's Cup &nbsp;·&nbsp; Season 18 2026</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if is_locked and not view_only:
        st.markdown('<div class="locked-banner">🔒 Squad is Locked</div>', unsafe_allow_html=True)

    # Determine edit_mode from session state (toggle is rendered in action bar below)
    if view_only:
        edit_mode = False
    else:
        edit_mode = st.session_state.get("edit_toggle", False) and not is_locked

    # Logo upload in edit mode
    if edit_mode:
        logo_up = st.file_uploader("Team Logo", key="logo_up_field", label_visibility="collapsed")
        if logo_up:
            team_logo = img_to_base64(logo_up)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # ===== SQUAD GRID + CAPTAIN =====
    main_col, cap_col = st.columns([3.8, 1.2])

    with main_col:
        # 3 rows × 6 columns = 18 slots (we use 17)
        for row in range(3):
            cols = st.columns(6)
            for col_i in range(6):
                idx_num = row * 6 + col_i
                if idx_num < 17:
                    idx = str(idx_num)
                    with cols[col_i]:
                        p_img = pics.get(idx)
                        num = idx_num + 1

                        # Build card HTML
                        if p_img:
                            img_html = f'<img src="data:image/jpeg;base64,{p_img}">'
                        else:
                            img_html = '''<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="card-empty-icon" style="width:50%;height:50%;">
                                <circle cx="12" cy="8" r="4" stroke="#4060a0" stroke-width="1.5"/>
                                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#4060a0" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>'''

                        name_html = (
                            f'<div class="card-name-text">{names[idx_num]}</div>'
                            if names[idx_num]
                            else '<div class="card-name-empty">Player</div>'
                        )

                        st.markdown(f"""
                            <div class="player-card-outer">
                                <div class="player-card-glow"></div>
                                <div class="player-card-inner">
                                    <div class="card-num">{num}</div>
                                    <div class="card-img-area">{img_html}</div>
                                    <div class="card-name-bar">{name_html}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        if edit_mode:
                            names[idx_num] = st.text_input(
                                "n", value=names[idx_num],
                                key=f"n{idx}", label_visibility="collapsed",
                                placeholder=f"Player {num}"
                            )
                            up = st.file_uploader("u", key=f"u{idx}", label_visibility="collapsed")
                            if up:
                                pics[idx] = img_to_base64(up)

    with cap_col:
        st.markdown('<div class="captain-section">', unsafe_allow_html=True)

        if cap_pic:
            cap_img_html = f'<img src="data:image/jpeg;base64,{cap_pic}">'
        else:
            cap_img_html = '''<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:45%;height:45%;opacity:0.15;">
                <circle cx="12" cy="8" r="4" stroke="#c8a84b" stroke-width="1.5"/>
                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#c8a84b" stroke-width="1.5" stroke-linecap="round"/>
            </svg>'''

        cap_name_display = cap_name if cap_name else "Captain"

        st.markdown(f"""
            <div class="captain-card-outer">
                <div class="captain-card-glow"></div>
                <div class="captain-card-inner">
                    <div class="captain-label">★ Captain ★</div>
                    <div class="captain-num">18</div>
                    <div class="captain-star">★</div>
                    <div class="captain-img-area">{cap_img_html}</div>
                    <div class="captain-name-bar">
                        <div class="captain-name-text">{cap_name_display}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if edit_mode:
            cap_name = st.text_input("cn", value=cap_name, key="cn",
                                     label_visibility="collapsed", placeholder="Captain Name")
            up_c = st.file_uploader("uc", key="uc", label_visibility="collapsed")
            if up_c:
                cap_pic = img_to_base64(up_c)

        st.markdown('</div>', unsafe_allow_html=True)

    # ===== ACTION BAR (always visible) =====
    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
    st.divider()
    if view_only:
        act_home, act_badge, act_spacer = st.columns([1, 1.2, 4])
        with act_home:
            if st.button("🏠 Home", key="home_btn", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
        with act_badge:
            st.markdown('<div class="view-mode-badge">👁 View Only</div>', unsafe_allow_html=True)
    else:
        act_home, act_edit, act_spacer, act_save = st.columns([1, 1.5, 2, 2])
        with act_home:
            if st.button("🏠 Home", key="home_btn", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
        with act_edit:
            edit_mode = st.toggle("✏️ EDIT MODE", value=False, disabled=is_locked, key="edit_toggle")
        with act_save:
            if edit_mode:
                if st.button("💾  Save All Changes", type="primary", use_container_width=True):
                    supabase.table("squads").update({
                        "captain_name": cap_name,
                        "player_list": names,
                        "squad_pics": pics,
                        "cap_pic": cap_pic,
                        "team_logo": team_logo
                    }).eq("team_name", team).execute()
                    st.success("✅ Squad saved successfully!")
                    st.rerun()
