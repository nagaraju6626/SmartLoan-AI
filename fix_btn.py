import re

with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix submit button text
content = content.replace('Sign In \ufffd+\'', 'Sign In &rarr;')
content = content.replace('Sign In +\'', 'Sign In &rarr;')
content = content.replace('Sign In +"', 'Sign In &rarr;')
# If it's literally "Sign In +'" in the file:
content = content.replace('Sign In +\'', 'Sign In &rarr;')
content = content.replace('Sign In →', 'Sign In &rarr;')

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(content)
