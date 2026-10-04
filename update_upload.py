import re

with open('frontend/pages/02_Data_Upload.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the place where the upload succeeds:
# st.success(f"Successfully uploaded {data_info['filename']}!")
pattern = r'st\.session_state\[\'current_dataset_name\'\] = data_info\[\'filename\'\]'

# Let's save the raw_df into session state
replacement = '''st.session_state['current_dataset_name'] = data_info['filename']
                    
                    # Store original raw dataset in session state to avoid local file dependency
                    uploaded_file.seek(0)
                    import pandas as pd
                    st.session_state['raw_df'] = pd.read_csv(uploaded_file)
                    uploaded_file.seek(0)
'''

content = content.replace(pattern, replacement)

with open('frontend/pages/02_Data_Upload.py', 'w', encoding='utf-8') as f:
    f.write(content)
