import os
import glob
import re

for file_path in glob.glob("frontend/pages/*.py"):
    if "01_Home.py" in file_path:
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check if already added
    if "render_header()" in content:
        continue
        
    # Replace render_sidebar() call with both imports if needed, and call both
    # Actually, they all import render_sidebar currently.
    content = content.replace(
        "from frontend.components.navigation import render_sidebar",
        "from frontend.components.navigation import render_sidebar\nfrom frontend.components.header import render_header"
    )
    
    content = content.replace(
        "render_sidebar()",
        "render_sidebar()\nrender_header()"
    )
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated all pages!")
