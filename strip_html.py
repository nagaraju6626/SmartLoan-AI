with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_markdown_html = False

for line in lines:
    if line.strip().startswith('st.markdown(f\"\"\"') or line.strip().startswith('st.markdown(\"\"\"'):
        in_markdown_html = True
        new_lines.append(line)
        continue
        
    if in_markdown_html:
        if line.strip() == '\"\"\", unsafe_allow_html=True)':
            in_markdown_html = False
            new_lines.append(line)
        else:
            # Completely strip leading whitespace for HTML lines to avoid Markdown code block parsing
            new_lines.append(line.lstrip())
    else:
        new_lines.append(line)

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
