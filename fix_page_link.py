import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the st.button with st.page_link
old_btn = r'if st\.button\(".*?Get Started", type="primary", use_container_width=False\):\s*st\.switch_page\("pages/02_Data_Upload\.py"\)'
new_btn = 'st.page_link("pages/02_Data_Upload.py", label="\U0001F680 Get Started")'

content = re.sub(old_btn, new_btn, content)

# Now update the CSS to target st.page_link instead of button[kind="primary"]
css_old = r'div\[data-testid="stHorizontalBlock"\]:nth-of-type\(2\) button\[kind="primary"\]'
css_new = r'div[data-testid="stHorizontalBlock"]:nth-of-type(2) [data-testid="stPageLink-NavLink"]'

content = content.replace(css_old, css_new)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
