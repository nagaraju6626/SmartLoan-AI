import re

with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    content = f.read()

css_replacements = {
    # Left Section Spacing
    ".left-content {\n    padding: 10px 40px;\n}": ".left-content {\n    padding: 0 40px;\n}",
    "margin-bottom: 24px;": "margin-bottom: 12px;",
    "font-size: 44px;": "font-size: 38px;",
    "margin-bottom: 16px;": "margin-bottom: 10px;",
    "margin-bottom: 32px;": "margin-bottom: 16px;",
    "font-size: 16px;": "font-size: 15px;",
    "gap: 20px;\n    margin-bottom: 20px;": "gap: 16px;\n    margin-bottom: 16px;",
    
    # Feature Items
    "margin-bottom: 20px;": "margin-bottom: 12px;",
    "color: #64748B;": "color: #475569;", # Slightly darker text for readability
    
    # Illustration
    "max-width: 320px;": "max-width: 290px;",
    
    # Bottom Benefits
    "gap: 24px;\n    margin-top: 20px;\n    border-top: 1px solid rgba(0,0,0,0.08);\n    padding-top: 20px;": "gap: 16px;\n    margin-top: 16px;\n    border-top: 1px solid rgba(0,0,0,0.08);\n    padding-top: 16px;",
    
    # Right Login Card
    "padding: 48px 40px !important;": "padding: 32px 32px !important;",
    "margin-bottom: 32px;": "margin-bottom: 20px;",
    "margin: 0 auto 20px auto;": "margin: 0 auto 12px auto;",
    "font-size: 26px;": "font-size: 24px;",
    
    # Footer in card
    "margin-top: 32px;\n    padding-top: 24px;": "margin-top: 20px;\n    padding-top: 16px;",
    
    # Grid gap
    "gap: 40px !important;": "gap: 30px !important;"
}

for old, new in css_replacements.items():
    content = content.replace(old, new)

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(content)
