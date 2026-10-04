import re

with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make submit button full width
content = content.replace('submit = st.form_submit_button("Sign In →")', 'submit = st.form_submit_button("Sign In →", use_container_width=True)')

# We need to replace the CSS with more compact padding/margins.
# Instead of complex regex, we can just replace specific rules:

css_replacements = {
    ".left-content {\n    padding: 40px 60px;\n}": ".left-content {\n    padding: 10px 40px;\n}",
    "margin-bottom: 50px;": "margin-bottom: 24px;",
    "font-size: 46px;": "font-size: 38px;",
    "margin-bottom: 20px;": "margin-bottom: 12px;",
    "font-size: 18px;": "font-size: 15px;",
    "margin-bottom: 40px;": "margin-bottom: 24px;",
    ".feature-list { margin-bottom: 40px; }": ".feature-list { margin-bottom: 20px; }",
    "margin-bottom: 24px;": "margin-bottom: 16px;",
    "width: 48px;\n    height: 48px;": "width: 40px;\n    height: 40px;",
    "font-size: 20px;": "font-size: 18px;",
    "max-width: 400px;": "max-width: 320px;",
    "margin: 20px auto;": "margin: 10px auto;",
    "gap: 32px;": "gap: 20px;",
    "padding-top: 24px;": "padding-top: 16px;",
    "padding: 50px 40px !important;": "padding: 40px 32px !important;",
    "gap: 40px !important;": "gap: 20px !important;",
    "width: 64px;\n    height: 64px;": "width: 54px;\n    height: 54px;",
    "font-size: 32px;": "font-size: 26px;",
    "font-size: 28px;": "font-size: 24px;",
    "font-size: 15px;": "font-size: 14px;"
}

# Apply replacements safely
for old, new in css_replacements.items():
    content = content.replace(old, new)

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(content)
