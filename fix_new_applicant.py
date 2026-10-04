import re

with open('frontend/pages/07_New_Applicant.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_load_sample = '''def load_sample(dataset_path, features):
    if dataset_path and os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)'''

new_load_sample = '''def load_sample(dataset_path, features):
    df = st.session_state.get('cleaned_df')
    if df is None:
        df = st.session_state.get('raw_df')
    if df is not None:'''

content = content.replace(old_load_sample, new_load_sample)

old_get_meta = '''def get_feature_metadata(dataset_path, features):
    meta = {}
    if not dataset_path or not os.path.exists(dataset_path):
        return meta
        
    df = pd.read_csv(dataset_path)'''

new_get_meta = '''def get_feature_metadata(dataset_path, features):
    meta = {}
    df = st.session_state.get('cleaned_df')
    if df is None:
        df = st.session_state.get('raw_df')
    if df is None:
        return meta'''

content = content.replace(old_get_meta, new_get_meta)

with open('frontend/pages/07_New_Applicant.py', 'w', encoding='utf-8') as f:
    f.write(content)
