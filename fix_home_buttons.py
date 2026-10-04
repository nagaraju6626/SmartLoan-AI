import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Current buttons:
# <a href="Data_Upload" target="_self" class="btn-primary">🚀 Get Started</a>
# <a href="Dashboard" target="_self" class="btn-secondary">▶ View Demo</a>

# We want to replace it with:
# <a href="javascript:void(0);" onclick="const link = Array.from(document.querySelectorAll('a')).find(el => el.href.endsWith('/Data_Upload') || el.href.includes('Data_Upload')); if(link) link.click();" class="btn-primary">🚀 Get Started</a>

js_click = "javascript:void(0);\" onclick=\"const link = Array.from(document.querySelectorAll('a')).find(el => el.href.endsWith('/Data_Upload') || el.href.includes('Data_Upload')); if(link) link.click();"

# Due to potential encoding issues with powershell, let's use python's powerful string replacement.
new_button = f'<a href="{js_click}" class="btn-primary">🚀 Get Started</a>'

# Find the hero-buttons div
pattern = r'<div class="hero-buttons">.*?</div>'

# Verify if we can find it
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, f'<div class="hero-buttons">\n{new_button}\n</div>', content, flags=re.DOTALL)
else:
    print("Could not find hero-buttons pattern!")

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
