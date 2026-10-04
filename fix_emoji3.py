with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The regex in previous step wrote the unicode character, but powershell might have mangled it before python executed it,
# or python wrote it properly but terminal is just displaying it wrong.
# Let's ensure it's written properly by using the explicit string.
content = content.replace('class="btn-primary">dYs? Get Started</a>', 'class="btn-primary">\\U0001F680 Get Started</a>')

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
