import re

with open('frontend/pages/04_Data_Analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update clean dataset button logic
old_clean = '''                    if clean_res.status_code == 200:
                        st.session_state['processed_dataset_id'] = dataset_id
                        st.session_state['processed_dataset_name'] = dataset_name
                        st.cache_data.clear()
                        st.rerun()'''

new_clean = '''                    if clean_res.status_code == 200:
                        st.session_state['processed_dataset_id'] = dataset_id
                        st.session_state['processed_dataset_name'] = dataset_name
                        
                        # Generate cleaned_df locally to avoid relying on backend filesystem
                        try:
                            from backend.ml.preprocessing import clean_dataset
                            st.session_state['cleaned_df'] = clean_dataset(raw_df)
                        except Exception as e:
                            st.error(f"Failed to process dataset locally: {e}")
                            
                        st.cache_data.clear()
                        st.rerun()'''

content = content.replace(old_clean, new_clean)

with open('frontend/pages/04_Data_Analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
