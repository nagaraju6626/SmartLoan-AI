import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the absolute link with a query parameter link, removing target="_self"
old_link = '<a href="/Data_Upload" target="_self" class="btn-primary">\\U0001F680 Get Started</a>'
new_link = '<a href="?action=get_started" class="btn-primary">\\U0001F680 Get Started</a>'

content = content.replace(old_link, new_link)

# Add the interception logic at the top of 01_Home.py, right after authentication
intercept_code = '''
# Intercept query parameter for Get Started button
if st.query_params.get("action") == "get_started":
    st.query_params.clear()
    st.switch_page("pages/02_Data_Upload.py")
'''

# Put it right after render_header()
content = content.replace('render_header()\n', 'render_header()\n' + intercept_code)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
