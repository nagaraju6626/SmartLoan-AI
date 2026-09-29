import re

file_path = "frontend/components/navigation.py"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Remove the button call completely
content = re.sub(r'st\.button\(.*?, on_click=toggle_sidebar, key="sidebar_toggle_btn"\)', '', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
