import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace get_active_dataset logic completely
old_get = '''def get_active_dataset():
    if 'processed_dataset_id' in st.session_state:
        ds_id = st.session_state['processed_dataset_id']
        if os.path.exists(os.path.join(PROCESSED_DIR, f"{ds_id}_cleaned.csv")) or os.path.exists(os.path.join(PROCESSED_DIR, f"{ds_id}.csv")):
            return ds_id, st.session_state.get('current_dataset_name', ds_id)
            
    try:
        if os.path.exists(PROCESSED_DIR):
            files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.csv')]
            if files:
                files.sort(key=lambda x: os.path.getmtime(os.path.join(PROCESSED_DIR, x)), reverse=True)
                latest_file = files[0]
                ds_id = latest_file.replace('_cleaned.csv', '').replace('.csv', '')
                # Restore to session state so it persists
                st.session_state['processed_dataset_id'] = ds_id
                st.session_state['current_dataset_id'] = ds_id
                st.session_state['processed_dataset_name'] = f"Dataset {ds_id[:6]}"
                return ds_id, st.session_state['processed_dataset_name']
    except Exception:
        pass
        
    return None, None'''

new_get = '''def get_active_dataset():
    if 'cleaned_df' in st.session_state or 'raw_df' in st.session_state:
        ds_id = st.session_state.get('current_dataset_id', 'unknown')
        ds_name = st.session_state.get('current_dataset_name', 'Unknown')
        return ds_id, ds_name
    return None, None'''

content = content.replace(old_get, new_get)

# Also fix the validation logic which does pd.read_csv
old_validation = '''        if not target_path:
            st.error("The active processed dataset could not be found. Please return to Data Upload and process the dataset again.")
        else:
            # 2. Validate dataset readability and content
            try:
                df = pd.read_csv(target_path)
                if len(df) == 0:
                    st.error("The processed dataset is empty. Please process the dataset again.")
                    target_path = None
            except Exception:
                st.error("The processed dataset could not be read. Please process the dataset again.")
                target_path = None'''

new_validation = '''        df = st.session_state.get('cleaned_df')
        if df is None:
            df = st.session_state.get('raw_df')
            
        if df is None:
            st.error("The active processed dataset could not be found. Please return to Data Upload and process the dataset again.")
        else:
            if len(df) == 0:
                st.error("The processed dataset is empty. Please process the dataset again.")
                df = None'''

content = content.replace(old_validation, new_validation)

# We also need to fix target_path variable references.
content = content.replace('target_path = get_target_path(dataset_id)', '# target_path replaced by session state')
content = content.replace('f"dataset_path={target_path}"', 'f"dataset_path=session_state"')
content = content.replace('file_path=target_path,', 'file_path="session_state",')

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
