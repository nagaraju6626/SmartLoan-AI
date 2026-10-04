import re

with open('frontend/components/navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS for the popover button to make it look like the sidebar-bottom
css_addition = '''
    /* Style the popover button to act as the fixed footer */
    [data-testid="stSidebar"] [data-testid="stPopover"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: inherit;
        border-top: 1px solid rgba(255,255,255,0.05);
        z-index: 100;
        padding: 0;
    }
    [data-testid="stSidebar"] [data-testid="stPopover"] > button {
        background-color: transparent !important;
        border: none !important;
        color: #94A3B8 !important;
        width: 100% !important;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        padding: 16px 20px !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stPopover"] > button:hover {
        color: white !important;
        background-color: rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebar"] [data-testid="stPopover"] p {
        font-size: 0.95rem !important;
        display: flex !important;
        align-items: center !important;
        margin: 0 !important;
    }
'''

content = content.replace('/* Bottom User Section */', css_addition + '\n    /* Bottom User Section */')

with open('frontend/components/navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)
