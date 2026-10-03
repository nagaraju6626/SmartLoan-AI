import re

file_path = 'frontend/components/theme.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS to inject
css_fix = """
    /* Force Hamburger Toggle Icon Visibility in ALL states */
    div[data-testid="column"]:nth-of-type(1) button p,
    div[data-testid="column"]:nth-of-type(1) button span,
    div[data-testid="column"]:nth-of-type(1) button svg {
        color: #334155 !important;
        fill: #334155 !important;
        stroke: #334155 !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
        text-indent: 0 !important;
    }
"""

# Insert right before the closing </style> of light_css
if '</style>' in content:
    # Find the last occurrence of </style>
    parts = content.rsplit('</style>', 1)
    content = parts[0] + css_fix + '    </style>' + parts[1]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS injected successfully.")
