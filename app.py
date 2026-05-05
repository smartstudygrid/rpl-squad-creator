import streamlit as st
from supabase import create_client, Client
import base64
import io
from PIL import Image

# --- 1. DATABASE CONNECTION ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Riyadh Premier League", layout="wide")

# --- 3. CUSTOM CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1531415074968-036ba1b575da?q=80&w=2070');
        background-size: cover;
    }}
    
    /* Top Center League Title */
    .header-center {{ 
        text-align: center; 
        width: 100%; 
        font-weight: bold; 
        font-size: 36px; 
        color: white; 
        padding-top: 20px;
        text-shadow: 2px 2px 4px #000;
        font-family: 'Arial Black', sans-serif;
    }}
    
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 14px; color: #ddd; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 12px; color: white; }}
    
    /* Team Name Style */
    .team-title {{
        color: white !important;
        font-family: "Arial Black", Gadget, sans-serif !important;
        font-weight: 900 !important;
        font-size: 42px !important;
        text-transform: uppercase;
        margin: 0;
    }}
    
    /* YELLOW THEME TOGGLE */
    .stWidgetLabel p {{ 
        color: white !important; 
        font-weight: bold !important; 
        font-size: 16px !important;
        background: #facc15 !important; /* Solid Yellow for Visibility */
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #854d0e;
    }}
    
    .squad-container {{ margin-top: -20px; }} /* Moved up to look better */
    
    /* Logo: CIRCLE */
    .logo-circle {{
        width: 110px; height: 110px; 
        background: rgba(255,255,255,0.2); 
        border: 3px solid #facc15;
        border-radius: 50%; 
        overflow: hidden; 
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0px 0px 15px rgba(250, 215, 0, 0.4);
    }}
    .logo-circle img {{ width: 100%; height: 100%; object-fit: cover; }}


    
    /* SQUARE Player Boxes */
    .img-box {{
        width: 110px; height: 110px; background: rgba(255,255,255,0.1); border: 2px solid #a3e635;
        border-radius: 4px; margin: 0 auto 5px auto; overflow: hidden;
        display: flex; align-items: center; justify-content: center;
    }}
    .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    .plain-name {{ color: white; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-top: 2px; text-align: center; }}

    /* Upload Icon - Matched to Yellow */
    .stFileUploader label {{ display: none; }}
    .stFileUploader section {{
        padding: 0 !important; min-height: unset !important; border: none !important; background: transparent !important;
    }}
    .stFileUploader section > div {{ display: none; }} 
    .stFileUploader button {{
        font-size: 0 !important; width: 32px !important; height: 32px !important;
        background-color: #facc15 !important; border-radius: 4px !important;
        border: 1px solid #854d0e !important; margin: 2px auto !important;
    }}
    .stFileUploader button::before {{ content: "↑"; font-size: 14px; color: #000; font-weight: bold; }}
    
    
    
   
    
    <div class="header-center">Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left">www.smartstudygrid.com</div>
""", unsafe_allow_html=True)

def img_to_base64(image_file):
    if image_file is None: return None
    img = Image.open(image_file).convert("RGB")
    img.thumbnail((300, 300)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

if 'page' not in st.session_state: st.session_state.page = 'home'
if 'team' not in st.session_state: st.session_state.team = None

# --- LOGIN SCREEN ---
if st.session_state.page == 'home':
    st.write("##")
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.write("##### Riyadh Premier League")
        t = st.selectbox("Select Your Team", ["Kaptan XI", "Pak Eagles", "Riyadh Badshahs", "Riyadh Mavericks", "Riyadh Stallions", "Wazirabad Stars"])
    p = st.text_input("Enter Password", type="password")
        if st.button("Enter Dashboard", use_container_width=True):
            # Passwords check here
            st.session_state.page = 'squad'; st.session_state.team = t; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- SQUAD SCREEN ---
elif st.session_state.page == 'squad':
    team = st.session_state.team
    st.markdown('<div class="squad-container"></div>', unsafe_allow_html=True)
    
    res = supabase.table("squads").select("*").eq("team_name", team).execute()
    db_data = res.data[0]
    is_locked = db_data['is_locked']
    names = db_data.get('player_list', [""]*17)
    pics = db_data.get('squad_pics', {}) 
    cap_name = db_data.get('captain_name', "Captain")
    cap_pic = db_data.get('cap_pic', None)
    team_logo = db_data.get('team_logo', None)

    # Upper Branding Area (Shifted Up)
    col_logo, col_title, col_edit = st.columns([0.8, 4.2, 1])
    
    with col_logo:
        if team_logo:
            st.markdown(f'<div class="logo-circle"><img src="data:image/jpeg;base64,{team_logo}"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="logo-circle"></div>', unsafe_allow_html=True)

    with col_title:
        st.markdown(f'<h1 class="team-title">{team}</h1>', unsafe_allow_html=True)
        
    edit_mode = col_edit.toggle("EDIT MODE", value=False, disabled=is_locked)

    m_col, c_col = st.columns([3, 1])

    with m_col:
        for r in range(3):
            cols = st.columns(6)
            for i in range(6):
                idx_num = (r * 6) + i
                if idx_num < 17:
                    idx = str(idx_num)
                    with cols[i]:
                        p_img = pics.get(idx)
                        if p_img:
                            st.markdown(f'<div class="img-box"><img src="data:image/jpeg;base64,{p_img}"></div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="img-box"></div>', unsafe_allow_html=True)
                        
                        st.markdown(f'<div class="plain-name">{names[idx_num] if names[idx_num] else "EMPTY"}</div>', unsafe_allow_html=True)
                        
                        if edit_mode:
                            names[idx_num] = st.text_input("n", value=names[idx_num], key=f"n{idx}", label_visibility="collapsed")
                            up = st.file_uploader("u", key=f"u{idx}", label_visibility="collapsed")
                            if up: pics[idx] = img_to_base64(up)

    with c_col:
        st.markdown('<div class="captain-frame">', unsafe_allow_html=True)
        # Redundant rectangle removed; star and text placed in gold badge
        st.markdown(f'<div class="captain-badge">⭐ CAPTAIN</div>', unsafe_allow_html=True)
        
        if cap_pic:
            st.markdown(f'<div class="img-box" style="width:180px; height:180px; border:4px solid #facc15;"><img src="data:image/jpeg;base64,{cap_pic}"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="img-box" style="width:180px; height:180px; border:4px solid #facc15;"></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="plain-name" style="font-size:20px;">{cap_name}</div>', unsafe_allow_html=True)
        
        if edit_mode:
            cap_name = st.text_input("cn", value=cap_name, key="cn", label_visibility="collapsed")
            up_c = st.file_uploader("uc", key="uc", label_visibility="collapsed")
            if up_c: cap_pic = img_to_base64(up_c)
        st.markdown('</div>', unsafe_allow_html=True)

    if edit_mode:
        if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True):
            supabase.table("squads").update({
                "captain_name": cap_name,
                "player_list": names,
                "squad_pics": pics,
                "cap_pic": cap_pic,
                "team_logo": team_logo
            }).eq("team_name", team).execute()
            st.success("Squad Saved Successfully!"); st.rerun()
