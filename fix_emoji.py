import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the mangled emoji with the correct one
# The mangled text is likely "dYs? Get Started" or something weird. Let's just replace the whole button string.
# We know the href and class.
pattern = r'<a href="javascript:void\(0\);" onclick="const link = Array.from\(document\.querySelectorAll\(\'a\'\)\)\.find\(el => el\.href\.endsWith\(\'/Data_Upload\'\) \|\| el\.href\.includes\(\'Data_Upload\'\)\); if\(link\) link\.click\(\);" class="btn-primary">.*?Get Started</a>'

new_button = '<a href="javascript:void(0);" onclick="const link = Array.from(document.querySelectorAll(\'a\')).find(el => el.href.endsWith(\'/Data_Upload\') || el.href.includes(\'Data_Upload\')); if(link) link.click();" class="btn-primary">\u1F680 Get Started</a>'.replace(r'\u1F680', '🚀')

content = re.sub(pattern, new_button, content)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
