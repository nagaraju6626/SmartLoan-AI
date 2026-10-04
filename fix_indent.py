import textwrap

with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_markdown_html = False

for line in lines:
    if line.strip() == 'st.markdown(f\"\"\"' or line.strip() == 'st.markdown(\"\"\"':
        in_markdown_html = True
        new_lines.append(line)
        continue
        
    if in_markdown_html:
        if line.strip() == '\"\"\", unsafe_allow_html=True)':
            in_markdown_html = False
            new_lines.append(line)
        else:
            # Strip up to 4 spaces or just lstrip if we want it completely left-aligned
            # Actually, just removing 4 spaces is enough, but to be safe, remove all leading spaces
            # wait, removing all leading spaces might break nested HTML readability, but it's fine for the parser
            # Let's remove 4 spaces
            if line.startswith('    '):
                new_lines.append(line[4:])
            else:
                new_lines.append(line)
    else:
        new_lines.append(line)

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
