import streamlit as st
from supabase import create_client, Client

# --- 1. DATABASE CONNECTION ---
# Ensure these match your Streamlit Secrets exactly
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

# --- 3. CUSTOM CSS (STYLING & LAYOUT) ---
st.markdown(f"""
    <style>
    /* Cricket Stadium Background */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Branding Elements */
    .header-left {{ position: absolute; top: 10px; left: 20px; font-weight: bold; font-size: 28px; color: #white; text-shadow: 2px 2px 4px #000; z-index: 999; }}
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 16px; color: #ddd; z-index: 999; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 14px; color: white; z-index: 999; background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 5px; }}
    
    /* Player & Captain Cards */
    .player-slot {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 5px;
    }}
    .player-name-tag {{
        background-color: #a3e635; /* Neon Green */
        color: #064e3b;
        font-weight: bold;
        padding: 6px;
        border-radius: 4px;
        font-size: 13px;
        text-transform: uppercase;
        margin-top: 8px;
    }}
    .captain-container {{
        background: rgba(255, 255, 255, 0.15);
        border: 4px solid #facc15; /* Gold Border */
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 20px rgba(250, 204, 21, 0.3);
    }}
    .captain-tag {{
        background-color: #a3e635;
        color: #064e3b;
        font-size: 26px;
        font-weight: 900;
        padding: 12px;
        border-radius: 8px;
        margin-top: 15px;
    }}
    
    /* Input field styling */
    input {{ background-color: rgba(255,255,255,0.9) !important; color: black !important; }}
    </style>
    
    <div class="header-left">🏏 Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left"><a href="http://www.smartstudygrid.com" style="color: #a3e635; text-decoration: none; font-weight:bold;">www.smartstudygrid.com</a></div>
""", unsafe_allow_html=True)

# --- 4. DATA LOGIC & AUTH ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'team' not in st.session_state:
    st.session_state.team = None

TEAMS_PASSWORDS = {
    "Kaptan XI": "kap11",
    "Pak Eagles": "eagle11",
    "Riyadh Badshahs": "king11",
    "Riyadh Mavericks": "mav11",
    "Riyadh Stallions": "stal11",
    "Wazirabad Stars": "star11"
}

# --- 5. NAVIGATION: HOME SCREEN ---
if st.session_state.page == 'home':
    st.write("##")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='background:rgba(0,0,0,0.6); padding:40px; border-radius:20px; border: 1px solid #444;'>", unsafe_allow_html=True)
        st.title("🏆 Squad Management")
        
        tab1, tab2 = st.tabs(["Team Login", "Admin Portal"])
        
        with tab1:
            team_sel = st.selectbox("Choose your team", list(TEAMS_PASSWORDS.keys()))
            team_p = st.text_input("Team Password", type="password", key="t_pass")
            if st.button("Login to Squad", use_container_width=True):
                if team_p == TEAMS_PASSWORDS[team_sel]:
                    st.session_state.page = 'squad'
                    st.session_state.team = team_sel
                    st.rerun()
                else:
                    st.error("Incorrect Password")
        
        with tab2:
            admin_p = st.text_input("Admin Key", type="password", key="a_pass")
            if st.button("Access Master Control", use_container_width=True):
                if admin_p == "admin123": # Change this to your preferred admin key
                    st.session_state.page = 'admin'
                    st.rerun()
                else:
                    st.error("Unauthorized Access")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. NAVIGATION: SQUAD EDITOR ---
elif st.session_state.page == 'squad':
    team = st.session_state.team
    
    # Secure Data Fetching
    response = supabase.table("squads").select("*").eq("team_name", team).execute()
    if len(response.data) == 0:
        st.error(f"Error: Team '{team}' not found in database. Please run SQL setup.")
        if st.button("Back"): st.session_state.page = 'home'; st.rerun()
        st.stop()
        
    team_data = response.data[0]
    is_locked = team_data.get('is_locked', False)
    players = team_data.get('player_list', [""] * 18)
    captain = team_data.get('captain_name', "")

    # Top Bar Actions
    c_top1, c_top2 = st.columns([4, 1])
    with c_top1:
        st.title(f"Editing: {team}")
    with c_top2:
        if st.button("🚪 Logout"):
            st.session_state.page = 'home'
            st.rerun()

    if is_locked:
        st.error("🔒 SYSTEM LOCKED: The Administrator has disabled updates. Viewing mode only.")

    # Main UI Grid (PDF Style)
    main_grid, cap_panel = st.columns([3, 1])

    with main_grid:
        # Row 1 & 2
        for r in range(2):
            cols = st.columns(6)
            for i in range(6):
                idx = (r * 6) + i
                with cols[i]:
                    st.markdown('<div class="player-slot"><div style="height:70px; width:70px; background:#555; border-radius:50%; margin:auto; border:2px solid #a3e635;"></div></div>', unsafe_allow_html=True)
                    players[idx] = st.text_input(f"P{idx}", value=players[idx], label_visibility="collapsed", disabled=is_locked)
                    st.markdown(f'<div class="player-name-tag">{players[idx] if players[idx] else "Empty"}</div>', unsafe_allow_html=True)
        
        # Row 3
        cols3 = st.columns(6)
        for i in range(6):
            idx = 12 + i
            with cols3[i]:
                st.markdown('<div class="player-slot"><div style="height:70px; width:70px; background:#555; border-radius:50%; margin:auto; border:2px solid #a3e635;"></div></div>', unsafe_allow_html=True)
                players[idx] = st.text_input(f"P{idx}", value=players[idx], label_visibility="collapsed", disabled=is_locked)
                st.markdown(f'<div class="player-name-tag">{players[idx] if players[idx] else "Empty"}</div>', unsafe_allow_html=True)

    with cap_panel:
        st.markdown('<div class="captain-container">', unsafe_allow_html=True)
        st.write("### ⭐️ CAPTAIN")
        st.markdown('<div style="height:200px; width:200px; background:#666; border-radius:50%; margin:auto; border:6px solid #facc15;"></div>', unsafe_allow_html=True)
        captain = st.text_input("Enter Captain Name", value=captain, disabled=is_locked)
        st.markdown(f'<div class="captain-tag">{captain if captain else "NAME HERE"}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("##")
        if st.button("💾 SAVE CHANGES", type="primary", use_container_width=True, disabled=is_locked):
            supabase.table("squads").update({
                "captain_name": captain, 
                "player_list": players
            }).eq("team_name", team).execute()
            st.success("Squad updated successfully!")
            st.balloons()

# --- 7. NAVIGATION: ADMIN MASTER CONTROL ---
elif st.session_state.page == 'admin':
    st.title("Master Admin Panel")
    
    # Check current lock status from any team
    res = supabase.table("squads").select("is_locked").limit(1).execute()
    current_lock = res.data[0]['is_locked'] if res.data else False
    
    status = "LOCKED" if current_lock else "OPEN"
    st.subheader(f"System Status: {status}")
    
    new_lock = st.toggle("Lock all squad updates", value=current_lock)
    
    if st.button("Apply Status to All Teams"):
        supabase.table("squads").update({"is_locked": new_lock}).neq("team_name", "").execute()
        st.success(f"System is now {'Locked' if new_lock else 'Open'}")
        
    if st.button("Return to Home"):
        st.session_state.page = 'home'
        st.rerun()
