import re

with open('frontend/components/header.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific st.popover line
# We can just define username first, then use it in the f-string.
# We will find the line: with st.popover...
pattern = re.compile(r'(with st\.popover\(f".*?\{st\.session_state\.get.*?\}, use_container_width=True\):)')

def replace_func(match):
    # This might be tricky because of the emojis, let's just do a string replace instead since we know the exact line content structure
    return 'username = st.session_state.get("username", "User")\n        with st.popover(f"👤 {username} ▾", use_container_width=True):'

# Or easier:
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'with st.popover(f"' in line and 'st.session_state.get(' in line:
        indent = line[:len(line) - len(line.lstrip())]
        lines[i] = f'{indent}username = st.session_state.get("username", "User")\n{indent}with st.popover(f"👤 {{username}} ▾", use_container_width=True):'

content = '\n'.join(lines)

with open('frontend/components/header.py', 'w', encoding='utf-8') as f:
    f.write(content)
