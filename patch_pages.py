import os

pages_dir = 'frontend/pages'
auth_code = '''
# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------
'''

for filename in os.listdir(pages_dir):
    if filename.endswith(".py") and filename != "00_Login.py":
        filepath = os.path.join(pages_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find where render_sidebar is called
        insert_idx = -1
        for i, line in enumerate(lines):
            if 'render_sidebar()' in line:
                insert_idx = i
                break
                
        if insert_idx != -1:
            lines.insert(insert_idx, auth_code + '\n')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Patched {filename}")
        else:
            print(f"Warning: render_sidebar() not found in {filename}")
