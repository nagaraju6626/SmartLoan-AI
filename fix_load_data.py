import re

with open('frontend/pages/04_Data_Analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace load_data function
old_load_data = '''@st.cache_data
def load_data(dataset_id):
    raw_df = None
    cleaned_df = None
    
    # Load Raw
    raw_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(dataset_id)]
    if raw_files:
        try:
            raw_df = pd.read_csv(os.path.join(UPLOAD_DIR, raw_files[0]))
        except Exception:
            pass
            
    # Load Cleaned
    cleaned_path = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
    if os.path.exists(cleaned_path):
        try:
            cleaned_df = pd.read_csv(cleaned_path)
        except Exception:
            pass
            
    return raw_df, cleaned_df'''

new_load_data = '''def load_data(dataset_id):
    # Fetch from session state as Streamlit Cloud does not share filesystem with the deployed backend
    raw_df = st.session_state.get('raw_df', None)
    cleaned_df = st.session_state.get('cleaned_df', None)
    return raw_df, cleaned_df'''

content = content.replace(old_load_data, new_load_data)

with open('frontend/pages/04_Data_Analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
