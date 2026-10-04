import codecs

with codecs.open("frontend/components/header.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace columns
content = content.replace(
    'col0, col1, col_spacer, col4 = st.columns([0.4, 5.0, 1.4, 1.2], vertical_alignment="center")',
    'col0, col1, col4 = st.columns([0.4, 6.1, 1.5], vertical_alignment="center")'
)

# Split at `    with col_spacer:`
parts = content.split('    with col_spacer:')
top_part = parts[0]

new_bottom = """    
    with col4:
        # User profile
        with st.popover("👤 Admin User ▾", use_container_width=True):
            st.markdown("👤 Profile")
            st.markdown("⚙️ Settings")
            st.markdown("🚪 Logout")
"""

content = top_part.rstrip() + "\n" + new_bottom

with codecs.open("frontend/components/header.py", "w", encoding="utf-8") as f:
    f.write(content)
