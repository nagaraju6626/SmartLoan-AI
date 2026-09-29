import streamlit as st
from frontend.components.theme import toggle_theme, apply_theme
from frontend.components.navigation import toggle_sidebar

def render_header():
    # apply_theme globally handles ALL CSS injection for light and dark modes!
    apply_theme()
    
    col0, col1, col2, col3, col4 = st.columns([0.4, 5, 0.7, 0.7, 1.2], vertical_alignment="center")
    
    with col0:
        st.button("☰", on_click=toggle_sidebar, use_container_width=True, key="header_sidebar_toggle")
        
    with col1:
        search_query = st.text_input("Search", placeholder="🔍 Search applicants, loans, reports...", label_visibility="collapsed")
    
    with col2:
        icon = "☀️" if st.session_state.theme == "dark" else "🌙"
        st.button(icon, on_click=toggle_theme, use_container_width=True, key="theme_toggle")
        
    with col3:
        with st.popover("🔔 •", use_container_width=True):
            st.markdown("**Notifications**")
            st.info("🔔 **New loan applications**\n\n3 new applications require review")
            st.success("📊 **Model update**\n\nLatest model evaluation completed")
            st.warning("⚠️ **Risk alert**\n\nHigh-risk applications detected")
            
    with col4:
        # User profile
        with st.popover("AD  ˅", use_container_width=True):
            st.markdown("**AD**\n\n*Administrator*")
            st.divider()
            st.markdown("👤 Profile")
            st.markdown("⚙️ Settings")
            st.markdown("🚪 Logout")

    if search_query:
        st.info(f"🔍 **Search Results for '{search_query}'**\n\nNo exact matches found in the current module. Try searching by Applicant ID.")
