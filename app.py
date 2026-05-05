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
    
    /* Branding & Toggle Visibility */
    .header-left {{ position: absolute; top: 10px; left: 20px; font-weight: bold; font-size: 26px; color: white; }}
    .header-right {{ position: absolute; top: 10px; right: 20px; font-size: 14px; color: #ddd; }}
    .footer-left {{ position: fixed; bottom: 10px; left: 10px; font-size: 12px; color: white; }}
    
    /* Force Toggle Text to White */
    .stWidgetLabel p {{ color: white !important; font-weight: bold !important; }}

    /* Layout */
    .squad-container {{ margin-top: 100px; }}
    .player-card {{ background: rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px; text-align: center; }}
    
    /* SQUARE Placeholders */
    .img-box {{
        width: 100px; height: 100px; background: #333; border: 2px solid #a3e635;
        border-radius: 6px; margin: 0 auto 5px auto; overflow: hidden;
        display: flex; align-items: center; justify-content: center;
    }}
    .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
    .name-tag {{ background: #a3e635; color: #000; font-weight: bold; padding: 3px; border-radius: 2px; font-size: 11px; text-transform: uppercase; }}

    /* Transparent Upload "Hyperlink" Style */
    .stFileUploader label {{ display: none; }}
    .stFileUploader section {{
        padding: 0 !important; min-height: unset !important; border: none !important; background: transparent !important;
    }}
    .stFileUploader button {{
        background: transparent !important; color: white !important; border: none !important; 
        text-decoration: underline !important; font-size: 12px !important; padding: 0 !important;
    }}
    .stFileUploader button::before {{ content: "Upload Player Pic"; }}
    
    .captain-frame {{ border: 4px solid #facc15; padding: 20px; border-radius: 15px; background: rgba(0,0,0,0.3); text-align: center; }}
    </style>
    
    <div class="header-left">Riyadh Premier League</div>
    <div class="header-right">Created by: Amanullah Khan</div>
    <div class="footer-left">www.smartstudygrid.com</div>
""", unsafe_allow_html=True)

# --- 4. IMAGE PROCESSING ---
def img_to_base64(image_file):
    if image_file is None: return None
    img = Image.open(image_file).convert("RGB")
    img.thumbnail((300, 300)) 
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- 5. NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'team' not in st.session_state: st.session_state.team = None

# --- HOME ---
if st.session_state.page == 'home':
    st.write("##")
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.title("🏆 RPL Login")
        t = st.selectbox("Select Team", ["Kaptan XI", "Pak Eagles", "Riyadh Badshahs", "Riyadh Mavericks", "Riyadh Stallions", "Wazirabad Stars"])
        p = st.text_input("Password", type="password")
        if st.button("Access Squad", use_container_width=True):
            st.session_state.page = 'squad'; st.session_state.team = t; st.rerun()

# --- SQUAD SCREEN ---
elif st.session_state.page == 'squad':
    team = st.session_state.team
    st.markdown('<div class="squad-container"></div>', unsafe_allow_html=True)
    
    # Data Fetch
    res = supabase.table("squads").select("*").eq("team_name", team).execute()
    db_data = res.data[0]
    is_locked = db_data['is_locked']
    names = db_data.get('player_list', [""]*18)
    pics = db_data.get('squad_pics', {}) 
    cap_name = db_data.get('captain_name', "Captain")
    cap_pic = db_data.get('cap_pic', None)

    col_title, col_edit, col_logout = st.columns([3, 1, 1])
    col_title.title(f"SQUAD: {team}")
    edit_mode = col_edit.toggle("EDIT MODE", value=False, disabled=is_locked)
    if col_logout.button("Logout"): st.session_state.page = 'home'; st.rerun()

    m_col, c_col = st.columns([3, 1])

    with m_col:
        for r in range(3):
            cols = st.columns(6)
            for i in range(6):
                idx = str((r * 6) + i)
                with cols[int(i)]:
                    p_img = pics.get(idx)
                    st.markdown(f'''<div class="img-box">
                        {f'<img src="data:image/jpeg;base64,{p_img}">' if p_img else ""}
                    </div>''', unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="name-tag">{names[int(idx)] if names[int(idx)] else "EMPTY"}</div>', unsafe_allow_html=True)
                    
                    if edit_mode:
                        names[int(idx)] = st.text_input("n", value=names[int(idx)], key=f"n{idx}", label_visibility="collapsed")
                        up = st.file_uploader("u", key=f"u{idx}", label_visibility="collapsed")
                        if up: pics[idx] = img_to_base64(up)

    with c_col:
        st.markdown('<div class="captain-frame">', unsafe_allow_html=True)
        st.write("### ⭐️ CAPTAIN")
        # Removed the extra box: Placeholder/Image appears immediately under the title
        st.markdown(f'''<div class="img-box" style="width:180px; height:180px; border:4px solid #facc15;">
            {f'<img src="data:image/jpeg;base64,{cap_pic}">' if cap_pic else ""}
        </div>''', unsafe_allow_html=True)
        
        st.markdown(f'<div class="name-tag" style="font-size:18px;">{cap_name}</div>', unsafe_allow_html=True)
        
        if edit_mode:
            cap_name = st.text_input("cn", value=cap_name, key="cn", label_visibility="collapsed")
            up_c = st.file_uploader("uc", key="uc", label_visibility="collapsed")
            if up_c: cap_pic = img_to_base64(up_c)
        st.markdown('</div>', unsafe_allow_html=True)

    if edit_mode:
        st.write("---")
        if st.button("💾 SAVE SQUAD PERMANENTLY"):
            supabase.table("squads").update({
                "captain_name": cap_name,
                "player_list": names,
                "squad_pics": pics,
                "cap_pic": cap_pic
            }).eq("team_name", team).execute()
            st.success("Squad & Photos Saved!"); st.rerun()
