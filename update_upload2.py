import re

with open('frontend/pages/02_Data_Upload.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Store original raw dataset in session state to avoid local file dependency
replacement = '''st.session_state['current_dataset_name'] = data_info['filename']
                    
                    # Store original raw dataset in session state
                    uploaded_file.seek(0)
                    import pandas as pd
                    st.session_state['raw_df'] = pd.read_csv(uploaded_file)
                    st.session_state['uploaded_filename'] = uploaded_file.name
                    uploaded_file.seek(0)
'''

# Use simple replace without regex escaping
content = content.replace("st.session_state['current_dataset_name'] = data_info['filename']", replacement)

with open('frontend/pages/02_Data_Upload.py', 'w', encoding='utf-8') as f:
    f.write(content)
