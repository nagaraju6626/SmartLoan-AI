import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('div[data-testid="stHorizontalBlock"]:nth-of-type(1)', 'div[data-testid="stHorizontalBlock"]:nth-of-type(2)')

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
