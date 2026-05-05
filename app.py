import streamlit as st
from supabase import create_client, Client
from PIL import Image
import io
import plotly.graph_objects as go

# --- 1. DATABASE CONNECTION ---
# Assumes you still have your Secrets set up in Streamlit Cloud
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
    
    /* FIXED OVERLAP: Added spacing for the top title */
    .fixed-header-space {{
        margin-top: 60px;
        display: block;
        height: 1px;
    }}
    
    /* Player & Captain Cards */
    .player-slot {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 5px;
        color: white;
    }}
    
    /* NEW: Modern Square Placeholder */
    .modern-placeholder {{
        height: 80px; 
        width: 80px; 
        background: #555; 
        border-radius: 10px; /* Modern Rounded Corners */
        margin: auto; 
        border: 2px solid #a3e635; /* Neon Green Border */
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
    
    /* NEW: Captain Placeholder is also square now */
    .captain-placeholder-large {{
        height: 200px; 
        width: 200px; 
        background: #666; 
        border-radius: 15px; /* Large Rounded Corners */
        margin: auto; 
        border: 6px solid #facc15; /* Gold Border */
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
    
    /* Hide some elements for the final print view */
    @media print {{
        .stButton {{ display: none !important; }}
        input {{ border: none !important; color: white !important; background: transparent !important;}}
    }}
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

# --- 5. HELPER FUNCTION FOR TEMPORARY PHOTO HANDLING ---
def handle_temp_photo(key_prefix, is_locked):
    # Streamlit cannot click on a placeholder to upload.
    # We must add an explicit upload button next to it.
    uploaded_file = st.file_uploader(
        "Set Profile Pic", 
        type=['png', 'jpg', 'jpeg'], 
        key=key_prefix + "_uploader", 
        disabled=is_locked, 
        label_visibility="collapsed"
    )
    if uploaded_file is not None:
        return Image.open(uploaded_file)
    else:
        return None

# --- 6. NAVIGATION: HOME SCREEN ---
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

# --- 7. NAVIGATION: SQUAD EDITOR (FIXED LAYOUT) ---
elif st.session_state.page == 'squad':
    # Add space to prevent overlap
    st.markdown('<div class="fixed-header-space"></div>', unsafe_allow_html=True)
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
    c_top1, c_top2, c_top3 = st.columns([3, 1, 1])
    with c_top1:
        st.title(f"Editing: {team}")
    with c_top2:
        # Added Print Feature: Preserves current state to download
        st.write("#")
        # st.button("Print Squad (PDF)") - Removed as PDF requires specific backend server.
        # Adding simple CSS-based download as a workaround.
        if st.button("Download as PDF", use_container_width=True):
            st.success("Please use your browser's print function (Ctrl+P or Cmd+P) to save as PDF. I have hidden the edit buttons for you.")

    with c_top3:
        st.write("#")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    if is_locked:
        st.error("🔒 SYSTEM LOCKED: The Administrator has disabled updates. Viewing mode only.")

    # Main UI Grid (PDF Style)
    main_grid, cap_panel = st.columns([3, 1])

    with main_grid:
        # Layout 18 players (3 rows of 6)
        for row in range(3):
            cols = st.columns(6)
            for i in range(6):
                idx = (row * 6) + i
                with cols[i]:
                    # Create unique state for each player pic
                    temp_pic = handle_temp_photo(f"P{idx}", is_locked)
                    
                    if temp_pic:
                        # Display the uploaded picture
                        st.image(temp_pic, use_container_width=True, width=80)
                    else:
                        # Display the square placeholder
                        st.markdown('<div class="player-slot"><div class="modern-placeholder"></div></div>', unsafe_allow_html=True)
                    
                    # Name Input (Linked to Database)
                    players[idx] = st.text_input(f"P{idx}_name", value=players[idx], label_visibility="collapsed", disabled=is_locked)
                    st.markdown(f'<div class="player-name-tag">{players[idx] if players[idx] else "Empty Slot"}</div>', unsafe_allow_html=True)

    with cap_panel:
        st.markdown('<div class="captain-container">', unsafe_allow_html=True)
        st.write("### ⭐️ CAPTAIN")
        
        # Captain Photo handling
        temp_cap_pic = handle_temp_photo("captain", is_locked)
        if temp_cap_pic:
            st.image(temp_cap_pic, use_container_width=True, width=200)
        else:
            st.markdown('<div class="captain-placeholder-large"></div>', unsafe_allow_html=True)
            
        # Captain Name
        captain = st.text_input("Enter Captain Name", value=captain, disabled=is_locked)
        st.markdown(f'<div class="captain-tag">{captain if captain else "CAPTAIN NAME"}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("##")
        if st.button("💾 SAVE CHANGES", type="primary", use_container_width=True, disabled=is_locked):
            # Photo saving requires Supabase Storage setup, which is not yet done.
            # We are currently only saving the text names.
            supabase.table("squads").update({
                "captain_name": captain, 
                "player_list": players
            }).eq("team_name", team).execute()
            st.success("Names saved! Remember, pictures are temporary until Storage is configured.")
            st.balloons()

# --- 8. NAVIGATION: ADMIN MASTER CONTROL ---
elif st.session_state.page == 'admin':
    # Add space to prevent overlap
    st.markdown('<div class="fixed-header-space"></div>', unsafe_allow_html=True)
    st.title("Master Admin Panel")
    
    # Check current lock status from any team
    try:
        res = supabase.table("squads").select("is_locked").limit(1).execute()
        current_lock = res.data[0]['is_locked'] if res.data else False
    except Exception:
        current_lock = False
    
    status = "LOCKED" if current_lock else "OPEN"
    st.subheader(f"System Status: {status}")
    
    new_lock = st.toggle("Lock all squad updates", value=current_lock)
    
    if st.button("Apply Status to All Teams"):
        supabase.table("squads").update({"is_locked": new_lock}).neq("team_name", "").execute()
        st.success(f"System is now {'Locked' if new_lock else 'Open'}")
        
    if st.button("Return to Home"):
        st.session_state.page = 'home'
        st.rerun()
