import re

with open('frontend/pages/14_Profile.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded Administrator role
role_logic = '''role = "Administrator" if st.session_state.get("email") == "admin@smartloan.com" else "User"
st.write(f"**Email:** {st.session_state.get('email', 'admin@smartloan.com')}")
st.write(f"**Role:** {role}")
'''

# The previous script only replaced part of the profile info, let's fix it properly.
content = re.sub(r'st\.write\("\*\*Role:\*\* Administrator"\)', role_logic, content)

# I should also conditionally show the info message
info_admin = 'st.info("This is the system administrator profile. You have full access to all Data Analysis, Model Training, and Applicant Risk Assessment tools within the Smart Loan platform.")'

new_info = '''if role == "Administrator":
    st.info("This is the system administrator profile. You have full access to all Data Analysis, Model Training, and Applicant Risk Assessment tools within the Smart Loan platform.")
else:
    st.info("This is your user profile. You can access the available Smart Loan tools from the sidebar.")'''

content = content.replace(info_admin, new_info)

with open('frontend/pages/14_Profile.py', 'w', encoding='utf-8') as f:
    f.write(content)
