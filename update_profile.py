import re

with open('frontend/pages/14_Profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

username = 'st.session_state.get("username", "Admin User")'
email = 'st.session_state.get("email", "admin@smartloan.com")'

content = re.sub(r'st\.subheader\("Admin User"\)', f'st.subheader({username})', content)
content = re.sub(r'st\.write\("\*\*Email:\*\* admin@smartloan.com"\)', f'st.write(f"**Email:** {{{email}}}")', content)

with open('frontend/pages/14_Profile.py', 'w', encoding='utf-8') as f:
    f.write(content)
