with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('label="dYs? Get Started"', 'label="\\U0001F680 Get Started"')

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
