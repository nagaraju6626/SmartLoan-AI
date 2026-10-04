import re

with open('frontend/components/navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the st.popover and its children block
pattern_popover = r'''\s*username\s*=\s*st\.session_state\.get\("username",\s*"User"\)\s*with\s*st\.popover\(f".*?",\s*use_container_width=True\):.*?st\.switch_page\("pages/00_Login\.py"\)'''
content = re.sub(pattern_popover, '', content, flags=re.DOTALL)

# 2. Remove the CSS styling for it
pattern_css1 = r'''\s*/\*\s*Style the popover button to act as the fixed footer\s*\*/.*?margin:\s*0\s*!important;\s*\}\}'''
content = re.sub(pattern_css1, '', content, flags=re.DOTALL)

pattern_css2 = r'''\s*/\*\s*Bottom User Section\s*\*/.*?\}\}'''
content = re.sub(pattern_css2, '', content, flags=re.DOTALL)

with open('frontend/components/navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)
