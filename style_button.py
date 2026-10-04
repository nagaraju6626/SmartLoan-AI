import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

btn_css = '''
/* Style the primary button to look like the old one */
div[data-testid="stHorizontalBlock"]:nth-of-type(2) button[kind="primary"] {
    background-color: #2563EB !important;
    color: white !important;
    padding: 4px 28px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.25) !important;
    transition: 0.2s !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(2) button[kind="primary"] p {
    font-size: 1.05rem !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(2) button[kind="primary"]:hover {
    background-color: #1D4ED8 !important;
}
</style>
'''

content = content.replace('</style>', btn_css)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
