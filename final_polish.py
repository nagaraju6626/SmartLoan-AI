with open('frontend/pages/00_Login.py', 'r', encoding='utf-8') as f:
    content = f.read()

css_replacements = {
    # Left Section Spacing
    "margin-bottom: 12px;": "margin-bottom: 8px;",
    "margin-bottom: 10px;": "margin-bottom: 6px;",
    "margin-bottom: 16px;": "margin-bottom: 12px;",
    
    # Feature Items
    "gap: 16px;\n    margin-bottom: 12px;": "gap: 12px;\n    margin-bottom: 10px;",
    "margin-top: 16px;\n    border-top: 1px solid rgba(0,0,0,0.08);\n    padding-top: 16px;": "margin-top: 12px;\n    border-top: 1px solid rgba(0,0,0,0.08);\n    padding-top: 12px;",
    "gap: 16px;": "gap: 12px;",
    
    # Card internal spacing
    "padding: 32px 32px !important;": "padding: 28px 28px !important;",
    "margin-bottom: 20px;": "margin-bottom: 16px;",
    "margin: 0 auto 12px auto;": "margin: 0 auto 10px auto;",
    
    # Grid Gap
    "gap: 30px !important;": "gap: 24px !important;"
}

for old, new in css_replacements.items():
    content = content.replace(old, new)

with open('frontend/pages/00_Login.py', 'w', encoding='utf-8') as f:
    f.write(content)
