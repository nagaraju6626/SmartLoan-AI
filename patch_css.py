with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('div[data-testid="stElementContainer"]:nth-child(1) input', '[data-testid="stForm"] div[data-testid="stElementContainer"]:nth-child(1) input')
content = content.replace('div[data-testid="stElementContainer"]:nth-child(2) input', '[data-testid="stForm"] div[data-testid="stElementContainer"]:nth-child(2) input')

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(content)
