import re

with open('frontend/pages/01_Home.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_kpis = '''        file_path = os.path.join("data/processed", f"{dataset_id}_cleaned.csv")
        if not os.path.exists(file_path):
            raw_files = [f for f in os.listdir("data/uploads") if f.startswith(dataset_id)]
            if not raw_files:
                return None
            file_path = os.path.join("data/uploads", raw_files[0])
            
        df = pd.read_csv(file_path)'''

new_kpis = '''        if 'cleaned_df' in st.session_state and st.session_state['cleaned_df'] is not None:
            df = st.session_state['cleaned_df']
        elif 'raw_df' in st.session_state and st.session_state['raw_df'] is not None:
            df = st.session_state['raw_df']
        else:
            return None'''

content = content.replace(old_kpis, new_kpis)

with open('frontend/pages/01_Home.py', 'w', encoding='utf-8') as f:
    f.write(content)
