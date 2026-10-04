import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

css_old1 = 'div[data-testid="stHorizontalBlock"]:nth-of-type(2) button[kind="primary"]'
css_new1 = 'div[data-testid="stHorizontalBlock"]:nth-of-type(2) [data-testid="stPageLink-NavLink"]'

content = content.replace(css_old1, css_new1)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
