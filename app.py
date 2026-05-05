import streamlit as st
from supabase import create_client, Client

# --- DATABASE CONNECTION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Riyadh Premier League", layout="wide", initial_sidebar_state="collapsed")

# --- CSS FOR THE EXACT PDF LAYOUT ---
st.markdown(f"""
    <style>
    /* Full-screen background */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1531415074968-036ba1b575da?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
    }}
    
    .header-left {{ position: absolute; top: 10px; left: 20px; font-weight: bold; font-size: 28px; color: #white; text-shadow: 2px 2px 4px #000; }}
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 16px; color: #ddd; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 14px; color: white; }}
    
    /* Grid Layout for Players */
    .player-slot {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }}
    .player-name {{
        background-color: #a3e635;
        color: #064e3b;
        font-weight: bold;
        padding: 5px;
        margin-top: 5px;
        border-radius: 4px;
        font-size: 14px;
    }}
    .captain-container {{
        background: rgba(255, 255, 255, 0.2);
        border: 3px solid #facc15;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }}
    .captain-name-tag {{
        background-color: #a3e635;
        color: #064e3b;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }}
    </style>
    
    <div class="header-left">🏏 Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left"><a href="http://www.smartstudygrid.com" style="color: white; text-decoration: none;">www.smartstudygrid.com</a></div>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'team' not in st.session_state:
    st.session_state.team = None

TEAMS = ["Kaptan XI", "Pak Eagles", "Riyadh Badshahs", "Riyadh Mavericks", "Riyadh Stallions", "Wazirabad Stars"]

# --- HOME SCREEN ---
if st.session_state.page == 'home':
    st.write("#")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div style='background:rgba(255,255,255,0.1); padding:40px; border-radius:20px; text-align:center;'>", unsafe_allow_html=True)
        st.subheader("Admin Portal")
        admin_p = st.text_input("Admin Password", type="password")
        if st.button("Login as Admin"):
            if admin_p == "admin123":
                st.session_state.page = 'admin'
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='background:rgba(255,255,255,0.1); padding:40px; border-radius:20px; text-align:center;'>", unsafe_allow_html=True)
        st.subheader("Team Login")
        team_sel = st.selectbox("Choose your team", TEAMS)
        team_p = st.text_input("Team Password", type="password")
        if st.button("Login to Squad"):
            # Simple check for demo; link to your database passwords in production
            if team_p != "":
                st.session_state.page = 'squad'
                st.session_state.team = team_sel
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- SQUAD SCREEN (Matching PDF Layout) ---
elif st.session_state.page == 'squad':
    team = st.session_state.team
    # Fetch Data
    team_data = supabase.table("squads").select("*").eq("team_name", team).single().execute().data
    is_locked = team_data.get('is_locked', False)
    players = team_data.get('player_list', [""] * 18)
    captain = team_data.get('captain_name', "Captain Name")

    st.title(f"{team} Squad")
    
    if is_locked:
        st.warning("⚠️ Updates Locked by Admin")

    # Layout Grid: 3 Rows of 6 Players, and a large Captain Slot
    # Total 18 small slots + 1 Large Captain Slot
    
    main_col, cap_col = st.columns([3, 1])

    with main_col:
        # Rows 1 & 2 (12 players)
        for row in range(2):
            cols = st.columns(6)
            for i in range(6):
                idx = (row * 6) + i
                with cols[i]:
                    st.markdown('<div class="player-slot"><div style="height:80px; width:80px; background:#ddd; border-radius:50%; margin:auto;"></div></div>', unsafe_allow_html=True)
                    players[idx] = st.text_input(f"Name {idx+1}", value=players[idx], label_visibility="collapsed", disabled=is_locked)
                    st.markdown(f'<div class="player-name">{players[idx] if players[idx] else "Empty"}</div>', unsafe_allow_html=True)
        
        # Row 3 (Remaining 5 players)
        cols3 = st.columns(6)
        for i in range(5):
            idx = 12 + i
            with cols3[i]:
                st.markdown('<div class="player-slot"><div style="height:80px; width:80px; background:#ddd; border-radius:50%; margin:auto;"></div></div>', unsafe_allow_html=True)
                players[idx] = st.text_input(f"Name {idx+1}", value=players[idx], label_visibility="collapsed", disabled=is_locked)
                st.markdown(f'<div class="player-name">{players[idx] if players[idx] else "Empty"}</div>', unsafe_allow_html=True)

    with cap_col:
        st.markdown('<div class="captain-container">', unsafe_allow_html=True)
        st.write("### CAPTAIN")
        st.markdown('<div style="height:250px; width:250px; background:#eee; border-radius:50%; margin:auto; border:5px solid #a3e635;"></div>', unsafe_allow_html=True)
        captain = st.text_input("Captain Name", value=captain, label_visibility="collapsed", disabled=is_locked)
        st.markdown(f'<div class="captain-name-tag">{captain}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Actions
    st.write("#")
    c1, c2, c3 = st.columns([1,1,1])
    if c2.button("💾 SAVE SQUAD", use_container_width=True) and not is_locked:
        supabase.table("squads").update({"captain_name": captain, "player_list": players}).eq("team_name", team).execute()
        st.success("Saved!")
    
    if st.button("⬅ Log Out"):
        st.session_state.page = 'home'
        st.rerun()

# --- ADMIN SCREEN ---
elif st.session_state.page == 'admin':
    st.subheader("Master Admin Control")
    if st.button("Toggle App Lock"):
        # Flip the lock for all teams
        new_val = not is_app_locked
        supabase.table("squads").update({"is_locked": new_val}).neq("team_name", "").execute()
        st.rerun()
    if st.button("Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
