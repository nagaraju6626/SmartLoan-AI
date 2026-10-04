import re

with open('frontend/pages/03_Dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_load = '''@st.cache_data
def load_dashboard_data(dataset_id):
    # Try processed first
    file_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    if not os.path.exists(file_path):
        raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
        if not raw_files:
            return None
        file_path = os.path.join(UPLOAD_DIR, raw_files[0])
    try:
        return pd.read_csv(file_path)
    except Exception:
        return None'''

new_load = '''def load_dashboard_data(dataset_id):
    if 'cleaned_df' in st.session_state and st.session_state['cleaned_df'] is not None:
        return st.session_state['cleaned_df']
    elif 'raw_df' in st.session_state and st.session_state['raw_df'] is not None:
        return st.session_state['raw_df']
    return None'''

content = content.replace(old_load, new_load)

with open('frontend/pages/03_Dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
