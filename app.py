# --- SAFER DATA FETCHING ---
res = supabase.table("squads").select("*").eq("team_name", team).execute()

if not res.data:
    st.error(f"⚠️ Error: Team '{team}' not found in the database.")
    st.info("Please run the SQL Setup in your Supabase dashboard to add the teams.")
    if st.button("Back to Login"):
        st.session_state.page = 'home'
        st.rerun()
    st.stop()  # This prevents the IndexError crash

db_data = res.data[0]
