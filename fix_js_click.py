import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

js_code = """javascript:void(0);" onclick="var links = document.querySelectorAll('[data-testid=\\'stPageLink-NavLink\\']'); var target = null; for(var i=0; i<links.length; i++) { if(links[i].textContent.includes('Data Upload')) { target = links[i]; break; } } if(target) { target.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window})); } else { window.location.href='Data_Upload'; }"""

# The current button in the file is:
# <a href="javascript:void(0);" onclick="const link = Array.from(document.querySelectorAll('a')).find(el => el.href.endsWith('/Data_Upload') || el.href.includes('Data_Upload')); if(link) link.click();" class="btn-primary">🚀 Get Started</a>

pattern = r'<a href="javascript:void\(0\);" onclick="const link =.*?Get Started</a>'
new_button = f'<a href="{js_code}" class="btn-primary">\U0001F680 Get Started</a>'

content = re.sub(pattern, new_button, content)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
