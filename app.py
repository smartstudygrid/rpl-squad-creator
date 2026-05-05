import streamlit as st
from supabase import create_client, Client
import base64
import io

# --- 1. DATABASE CONNECTION ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Connection Error: Please check your Streamlit Secrets for SUPABASE_URL and SUPABASE_KEY.")
    st.stop()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Riyadh Premier League", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 3. CUSTOM CSS (VISUAL POLISH) ---
st.markdown(f"""
    <style>
    /* Background & Overlap Spacing */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
    }}
    
    .fixed-header-space {{ margin-top: 60px; display: block; height: 1px; }}

    /* Branding */
    .header-left {{ position: absolute; top: 10px; left: 20px; font-weight: bold; font-size: 28px; color: #white; text-shadow: 2px 2px 4px #000; z-index: 999; }}
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 16px; color: #ddd; z-index: 999; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 14px; color: white; z-index: 999; background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 5px; }}
    
    /* SQUARE Placeholders */
    .modern-placeholder {{
        height: 80px; width: 80px; background: #555; 
        border-radius: 10px; margin: auto; 
        border: 2px solid #a3e635; /* Neon Green Border */
    }}
    .captain-placeholder-large {{
        height: 200px; width: 200px; background: #666; 
        border-radius: 15px; margin: auto; 
        border: 6px solid #facc15; /* Gold Border */
    }}

    /* Name Labels */
    .player-slot {{ background: rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; text-align: center; color: white; }}
    .player-name-tag {{ background-color: #a3e635; color: #064e3b; font-weight: bold; padding: 6px; border-radius: 4px; font-size: 13px; text-transform: uppercase; margin-top: 8px; min-height: 30px;}}
    .captain-container {{ background: rgba(255, 255, 255, 0.15); border: 4px solid #facc15; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 0 20px rgba(250, 204, 21, 0.3); }}
    .captain-tag {{ background-color: #a3e635; color: #064e3b; font-size: 26px; font-weight: 900; padding: 12px; border-radius: 8px; margin-top: 15px; }}
    
    /* Simplified Square Upload Icon */
    .stFileUploader label {{ display: none; }}
    .stFileUploader section {{ max-width: 35px !important; min-height: 35px !important; padding: 0 !important; margin: 0 auto !important; border: none !important; background: transparent !important; }}
    .stFileUploader section > div {{ display: none; }} /* Hides text */
    .stFileUploader button {{
        font-size: 0 !important; width: 30px !important; height: 30px !important;
        background-color: #a3e635 !important; border-radius: 4px !important; /* Square Icon */
        border: 1px solid #064e3b !important;
    }}
    .stFileUploader button::before {{ content: "⬆"; font-size: 16px; color: #064e3b; }}

    /* Input field styling */
    input {{ background-color: rgba(255,255,255,0.9) !important; color: black !important; }}
    </style>
    
    <div class="header-left">🏏 Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left"><a href="http://www.smartstudygrid.com" style="color: #a3e635; text-decoration: none; font-weight:bold;">www.smartstudygrid.com</a></div>
""", unsafe_allow_html=True)

# --- 4. AUTH & NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'team' not in st.session_state: st.session_state.team = None

TEAMS_PASSWORDS = { "Kaptan XI": "kap11", "Pak Eagles": "eagle11", "Riyadh Badshahs": "king11", "Riyadh Mavericks": "mav11", "Riyadh Stallions": "stal11", "Wazirabad Stars": "star11" }

# --- HOME SCREEN ---
if st.session_state.page == 'home':
    st.write("##")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='background:rgba(0,0,0,0.6); padding:40px; border-radius:20px;'>", unsafe_allow_html=True)
        st.title("🏆 Squad Management")
        team_sel = st.selectbox("Choose team", list(TEAMS_PASSWORDS.keys()))
        team_p = st.text_input("Password", type="password", key="t_pass")
        if st.button("Login", use_container_width=True):
            if team_p == TEAMS_PASSWORDS[team_sel]:
                st.session_state.page = 'squad'; st.session_state.team = team_sel; st.rerun()
            else: st.error("Incorrect Password")
        st.markdown("</div>", unsafe_allow_html=True)

# --- SQUAD SCREEN (FIXED OVERLAP & NAMES) ---
elif st.session_state.page == 'squad':
    st.markdown('<div class="fixed-header-space"></div>', unsafe_allow_html=True)
    team = st.session_state.team
    
    # Secure Data Fetching
    response = supabase.table("squads").select("*").eq("team_name", team).execute()
    if len(response.data) == 0:
        st.error(f"Error: Team '{team}' not found. Please run SQL setup."); st.stop()
        
    team_data = response.data[0]
    is_locked = team_data.get('is_locked', False)
    players = team_data.get('player_list', [""] * 18)
    captain = team_data.get('captain_name', "")

    # Top Bar Actions
    c_top1, c_top2, c_top3 = st.columns([3, 1, 1])
    with c_top1: st.title(f"Editing: {team}")
    with c_top2:
        # Solution: VIEW/EDIT Toggle to solve "Names Twice" problem
        edit_mode = st.toggle("Edit Mode", key="edit_toggle", disabled=is_locked)
    with c_top3:
        if st.button("🚪 Logout", use_container_width=True): st.session_state.page = 'home'; st.rerun()

    if is_locked: st.error("🔒 SYSTEM LOCKED: updates disabled.")

    # Main UI Grid (PDF Style)
    main_grid, cap_panel = st.columns([3, 1])

    with main_grid:
        # Layout 18 players (3 rows of 6)
        for row in range(3):
            cols = st.columns(6)
            for i in range(6):
                idx = (row * 6) + i
                with cols[i]:
                    # Display Square Placeholder or Image (Needs Bucket storage)
                    # We continue using placeholder for now as stable storage isn't configured
                    st.markdown('<div class="player-slot"><div class="modern-placeholder"></div></div>', unsafe_allow_html=True)
                    if edit_mode:
                        st.file_uploader("up", key=f"u{idx}", label_visibility="collapsed")

                    # Name Label (Always Visible)
                    st.markdown(f'<div class="player-name-tag">{players[idx] if players[idx] else "NAME HERE"}</div>', unsafe_allow_html=True)
                    
                    # Name Input (Visible only in Edit Mode)
                    if edit_mode:
                        players[idx] = st.text_input(f"P{idx}", value=players[idx], label_visibility="collapsed")

    with cap_panel:
        st.markdown('<div class="captain-container">', unsafe_allow_html=True)
        st.write("### ⭐️ CAPTAIN")
        # Captain Photo handling (Bucket storage required)
        st.markdown('<div class="captain-placeholder-large"></div>', unsafe_allow_html=True)
        if edit_mode:
            st.file_uploader("cup", key="uc", label_visibility="collapsed")
            
        # Captain Name Label (Always Visible)
        st.markdown(f'<div class="captain-tag">{captain if captain else "CAPTAIN NAME"}</div>', unsafe_allow_html=True)
        
        # Name Input (Visible only in Edit Mode)
        if edit_mode:
            captain = st.text_input("Enter Captain Name", value=captain)

        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("##")
        if edit_mode and st.button("💾 SAVE CHANGES", type="primary", use_container_width=True):
            supabase.table("squads").update({ "captain_name": captain, "player_list": players }).eq("team_name", team).execute()
            st.success("Squad updated!"); st.balloons()
