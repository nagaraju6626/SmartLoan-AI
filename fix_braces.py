import re

with open('frontend/components/navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to escape all { and } in the recently added CSS block
# Let's find the block starting from "/* Style the popover button to act as the fixed footer */"
# and ending at "/* Bottom User Section */"

start_idx = content.find('/* Style the popover button to act as the fixed footer */')
end_idx = content.find('/* Bottom User Section */', start_idx)

if start_idx != -1 and end_idx != -1:
    block = content[start_idx:end_idx]
    
    # Escape braces (but block might already have some escaped? No, it was added as raw string in my script, but injected into the python file which uses it as an f-string body)
    block_escaped = block.replace('{', '{{').replace('}', '}}')
    
    content = content[:start_idx] + block_escaped + content[end_idx:]

with open('frontend/components/navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)
