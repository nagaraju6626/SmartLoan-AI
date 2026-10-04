import re

with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to match the specific popover line.
# Note: due to powershell/terminal charset issues, the string in cat was "dY  Admin User -_"
# but in the actual file it's likely "👤 Admin User ▾".
# I'll just use regex to replace it.
content = re.sub(
    r'st\.popover\("([^"]+)Admin User([^"]+)",\s*use_container_width=True\)', 
    r'st.popover(f"\1{st.session_state.get(\'username\', \'User\')}\2", use_container_width=True)', 
    content
)

# Alternative just in case:
content = re.sub(
    r'st\.popover\(".*?Admin User.*?",\s*use_container_width=True\)',
    r'st.popover(f"👤 {st.session_state.get(\'username\', \'User\')} ▾", use_container_width=True)',
    content
)

with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
