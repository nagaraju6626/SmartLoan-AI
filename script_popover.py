import codecs
import re

with codecs.open("frontend/components/header.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace col4 block
col4_pattern = re.compile(r'    with col4:\n        # User profile\n        with st\.popover\(".*?Admin User.*?", use_container_width=True\):\n.*?st\.markdown\(.*?Logout"\)', re.DOTALL)

new_col4 = """    with col4:
        # User profile
        with st.popover("👤 Admin User ▾", use_container_width=True):
            st.page_link("pages/14_Profile.py", label="Profile", icon="👤")
            st.page_link("pages/13_Settings.py", label="Settings", icon="⚙️")
            if st.button("🚪 Logout", use_container_width=True):
                # Safe logout flow
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state["logged_out"] = True
                st.switch_page("pages/01_Home.py")"""

content = col4_pattern.sub(new_col4, content)

with codecs.open("frontend/components/header.py", "w", encoding="utf-8") as f:
    f.write(content)
