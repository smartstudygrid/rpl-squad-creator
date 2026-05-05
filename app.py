import streamlit as st
from supabase import create_client, Client
import base64

# --- 1. DATABASE CONNECTION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Riyadh Premier League", layout="wide")

# --- 3. ADVANCED CSS (FIXING THE MESS) ---
st.markdown(f"""
    <style>
    /* Background & Global spacing */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=2070');
        background-size: cover;
    }}
    
    /* Branding Fixes */
    .header-left {{ position: absolute; top: 10px; left: 20px; font-weight: bold; font-size: 24px; color: white; }}
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 14px; color: #ccc; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 12px; color: white; }}

    /* Layout Spacing to prevent overlap */
    .squad-container {{ margin-top: 80px; }}

    /* SQUARE Player Cards */
    .player-card {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        min-height: 180px;
    }}
    .player-img-square {{
        width: 100px;
        height: 100px;
        background: #444;
        border: 2px solid #a3e635;
        border-radius: 4px; /* Square with slight roundness */
        margin: 0 auto 10px auto;
        object-fit: cover;
    }}
    .name-label {{
        background: #a3e635;
        color: #000;
        font-weight: bold;
        padding: 4px;
        border-radius: 2px;
        text-transform: uppercase;
        font-size: 12px;
    }}

    /* Shrinking the Upload Button */
    .stFileUploader section {{ padding: 0 !important; }}
    .stFileUploader label {{ display: none; }}
    
    /* Captain Box */
    .captain-box {{
        border: 4px solid #facc15;
        padding: 20px;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
        text-align: center;
    }}
    </style>
    
    <div class="header-left">Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left">www.smartstudygrid.com</div>
""", unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'team' not in st.session_state: st.session_state.team = None

TEAMS = ["Kaptan XI", "Pak Eagles", "Riyadh Badshahs", "Riyadh Mavericks", "Riyadh Stallions", "Wazirabad Stars"]

# --- HOME ---
if st.session_state.page == 'home':
    st.write("#")
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.title("League Login")
        t = st.selectbox("Team", TEAMS)
        p = st.text_input("Password", type="password")
        if st.button("Enter Dashboard", use_container_width=True):
            st.session_state.page = 'squad'
            st.session_state.team = t
            st.rerun()

# --- SQUAD EDITOR ---
elif st.session_state.page == 'squad':
    team = st.session_state.team
    st.markdown('<div class="squad-container"></div>', unsafe_allow_html=True)
    
    # Fetch Data
    res = supabase.table("squads").select("*").eq("team_name", team).execute()
    data = res.data[0]
    is_locked = data['is_locked']
    players = data.get('player_list', [""]*18)
    captain = data.get('captain_name', "Name")

    col_title, col_logout = st.columns([4, 1])
    col_title.title(f"SQUAD: {team}")
    if col_logout.button("Logout"): 
        st.session_state.page = 'home'
        st.rerun()

    # --- THE GRID ---
    m_col, c_col = st.columns([3, 1])

    with m_col:
        for r in range(3):
            cols = st.columns(6)
            for i in range(6):
                idx = (r * 6) + i
                with cols[i]:
                    st.markdown(f'<div class="player-card"><div class="player-img-square"></div><div class="name-label">{players[idx]}</div></div>', unsafe_allow_html=True)
                    # Small input only if not locked
                    if not is_locked:
                        players[idx] = st.text_input(f"edit_{idx}", value=players[idx], label_visibility="collapsed")
                        st.file_uploader("up", key=f"up_{idx}", label_visibility="collapsed")

    with c_col:
        st.markdown('<div class="captain-box">', unsafe_allow_html=True)
        st.write("### CAPTAIN")
        st.markdown('<div class="player-img-square" style="width:180px; height:180px; border:5px solid #facc15;"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="name-label" style="font-size:20px;">{captain}</div>', unsafe_allow_html=True)
        if not is_locked:
            captain = st.text_input("CapName", value=captain, label_visibility="collapsed")
            st.file_uploader("cap_up", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ACTIONS ---
    st.write("---")
    a1, a2, a3 = st.columns(3)
    if a1.button("💾 SAVE DATA") and not is_locked:
        supabase.table("squads").update({"captain_name": captain, "player_list": players}).eq("team_name", team).execute()
        st.success("Saved!")
    
    # Simple Screenshot Instruction for the User
    a2.info("📸 To download as image: Press **Cmd+Shift+4** (Mac) or **Windows+Shift+S** (PC)")
