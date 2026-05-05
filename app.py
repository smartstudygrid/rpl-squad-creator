import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURATION & BRANDING ---
st.set_page_config(page_title="Riyadh Premier League", layout="wide")

# Custom CSS for the "Sporty" Look and Header/Footer Requirements
st.markdown(f"""
    <style>
    .main {{ background-color: #f0f2f6; }}
    .header-left {{ position: absolute; top: -50px; left: 0; font-weight: bold; font-size: 24px; color: #1e3a8a; }}
    .header-right {{ position: absolute; top: -50px; right: 0; font-size: 14px; color: #666; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 12px; }}
    .captain-card {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 3px solid #ffd700; }}
    .player-card {{ background: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center; }}
    </style>
    <div class="header-left">Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left"><a href="https://www.smartstudygrid.com">www.smartstudygrid.com</a></div>
""", unsafe_allow_html=True)

# --- DATABASE MOCKUP (Replace with Supabase for permanent storage) ---
# For now, this uses Streamlit Session State to demonstrate the logic
if 'app_locked' not in st.session_state:
    st.session_state.app_locked = False

TEAMS = {
    "Kaptan XI": "pass123",
    "Pak Eagles": "pass456",
    "Riyadh Badshahs": "pass789",
    "Riyadh Mavericks": "mavs2026",
    "Riyadh Stallions": "stallion1",
    "Wazirabad Stars": "wazir1"
}

# --- ADMIN PANEL (Hidden Sidebar) ---
with st.sidebar:
    st.header("⚙️ Admin Control")
    admin_pass = st.text_input("Admin Password", type="password")
    if admin_pass == "admin123": # Change this!
        st.session_state.app_locked = st.checkbox("Lock App (Disable Updates)", value=st.session_state.app_locked)
        if st.session_state.app_locked:
            st.error("SQUAD UPDATES ARE LOCKED")
        else:
            st.success("SQUAD UPDATES ARE OPEN")

# --- MAIN INTERFACE ---
st.title("🏆 Squad Management Portal")

# 1. Team Selection
team_choice = st.selectbox("Select your Team", ["---"] + list(TEAMS.keys()))

if team_choice != "---":
    password = st.text_input(f"Enter Password for {team_choice}", type="password")
    
    if password == TEAMS[team_choice]:
        st.success(f"Welcome, Captain of {team_choice}!")
        
        if st.session_state.app_locked:
            st.warning("⚠️ The Administrator has locked squad updates. You can view but not edit.")

        # --- UPLOAD SECTION ---
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Team Identity")
            logo = st.file_uploader("Upload Team Logo", disabled=st.session_state.app_locked)
            cap_pic = st.file_uploader("Upload Captain's Picture (Prominent)", disabled=st.session_state.app_locked)
            cap_name = st.text_input("Captain Name", disabled=st.session_state.app_locked)

        with col2:
            st.subheader("Squad Members (18 Total)")
            player_data = []
            for i in range(1, 19):
                name = st.text_input(f"Player {i} Name", key=f"p{i}", disabled=st.session_state.app_locked)
                # In a live app, you'd add a file_uploader for each player here

        # --- VISUAL DISPLAY (The "Enhancement") ---
        st.divider()
        st.header(f"Final Squad: {team_choice}")
        
        # Display Captain
        c_col1, c_col2, c_col3 = st.columns([1, 1, 1])
        with c_col2:
            st.markdown(f'<div class="captain-card"><h3>CAPTAIN</h3><h2>{cap_name if cap_name else "Assign Captain"}</h2></div>', unsafe_allow_html=True)
            if cap_pic:
                st.image(cap_pic, use_container_width=True)

        # Display Players in a Grid
        st.subheader("Team Players")
        cols = st.columns(3)
        for i in range(1, 19):
            with cols[(i-1) % 3]:
                st.markdown(f'<div class="player-card"><b>Player {i}</b><br>{st.session_state.get(f"p{i}", "Empty Slot")}</div>', unsafe_allow_html=True)
                st.write("") # Spacer

    elif password != "":
        st.error("Incorrect Password")

else:
    st.info("Please select your team from the dropdown to manage your squad.")
