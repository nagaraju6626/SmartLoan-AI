import re

with open('frontend/components/navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

username_logic = '''
        username = st.session_state.get("username", "User")
        with st.popover(f"👤 {username}", use_container_width=True):
            st.page_link("pages/14_Profile.py", label="Profile", icon="👤")
            st.page_link("pages/13_Settings.py", label="Settings", icon="⚙️")
            if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state["logged_out"] = True
                st.switch_page("pages/00_Login.py")
'''

# Remove the old HTML Admin Bottom
html_bottom = '''
        # Admin Bottom
        st.markdown("""
        <div class="sidebar-bottom">
            <div class="user-info">
                <span>dY </span>
                <span>Admin User</span>
            </div>
            <span class="settings-icon">sT,?</span>
        </div>
        """, unsafe_allow_html=True)
'''

# Since encoding issues might prevent simple string matching, let's use regex
content = re.sub(r'# Admin Bottom\s*st\.markdown\("""\s*<div class="sidebar-bottom">.*?</div>\s*""", unsafe_allow_html=True\)', username_logic, content, flags=re.DOTALL)

with open('frontend/components/navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)
