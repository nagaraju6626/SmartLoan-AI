import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace get_active_dataset completely using regex to match whatever it currently is
pattern = r'def get_active_dataset\(\):.*?return None, None'

new_get = '''def get_active_dataset():
    if 'cleaned_df' in st.session_state or 'raw_df' in st.session_state:
        ds_id = st.session_state.get('processed_dataset_id', st.session_state.get('current_dataset_id'))
        ds_name = st.session_state.get('processed_dataset_name', st.session_state.get('current_dataset_name', 'Unknown'))
        return ds_id, ds_name
    return None, None'''

content = re.sub(pattern, new_get, content, flags=re.DOTALL)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
