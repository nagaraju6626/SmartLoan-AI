import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_load = '''@st.cache_data
def load_data(dataset_id):
    file_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    is_cleaned = True
    if not os.path.exists(file_path):
        is_cleaned = False
        raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
        if not raw_files:
            return None, False
        file_path = os.path.join(UPLOAD_DIR, raw_files[0])
    try:
        return pd.read_csv(file_path), is_cleaned
    except Exception:
        return None, False'''

new_load = '''def load_data(dataset_id):
    if 'cleaned_df' in st.session_state and st.session_state['cleaned_df'] is not None:
        return st.session_state['cleaned_df'], True
    elif 'raw_df' in st.session_state and st.session_state['raw_df'] is not None:
        return st.session_state['raw_df'], False
    return None, False'''

content = content.replace(old_load, new_load)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)
