import streamlit as st
import httpx
import os
import pandas as pd

try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://127.0.0.1:8000"))
except Exception:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

def get_active_dataset():
    if 'processed_dataset_id' in st.session_state:
        return st.session_state['processed_dataset_id'], st.session_state.get('processed_dataset_name', 'Unknown')
        
    if 'current_dataset_id' in st.session_state:
        ds_id = st.session_state['current_dataset_id']
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
                st.session_state['processed_dataset_name'] = latest_file
                return ds_id, latest_file
    except Exception:
        pass
        
    return None, None

st.title("Business Reports")
st.markdown("Generate and download comprehensive reports for loan applications.")

dataset_id, dataset_name = get_active_dataset()

if not dataset_id:
    st.warning("No processed dataset is available. Please upload and process a dataset before generating a report.")
else:
    st.info(f"Generating reports for dataset: {dataset_name}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Report Type:** Business Report")
        report_type = "business_report"
    with col2:
        if "report_format" not in st.session_state:
            st.session_state["report_format"] = "pdf"
        report_format = st.selectbox("Format", ["pdf"], key="report_format")
        
    if st.button("Generate Report"):
        # 1. Validate dataset existence
        file_path_cleaned = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
        file_path_fallback = os.path.join(PROCESSED_DIR, f"{dataset_id}.csv")
        
        target_path = None
        if os.path.exists(file_path_cleaned):
            target_path = file_path_cleaned
        elif os.path.exists(file_path_fallback):
            target_path = file_path_fallback
            
        if not target_path:
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
                target_path = None
                
        if target_path:
            with st.spinner("Generating report..."):
                try:
                    prediction_inputs = None
                    prediction_result = None
                    active_ver = st.session_state.get('active_model_version')
                    
                    if st.session_state.get('prediction_submitted'):
                        prediction_inputs = st.session_state.get('submitted_prediction_inputs')
                        prediction_result = st.session_state.get('prediction_result')
    
                    payload = {
                        "dataset_id": dataset_id,
                        "format": report_format,
                        "active_model_version": active_ver,
                        "prediction_result": prediction_result,
                        "prediction_inputs": prediction_inputs
                    }
                    res = httpx.post(f"{API_BASE_URL}/api/reports/generate", json=payload, timeout=30.0)
                    if res.status_code == 200:
                        data = res.json()
                        st.success("Report generated successfully!")
    
                        download_url = f"{API_BASE_URL}{data['download_url']}"
                        st.session_state["report_download_url"] = download_url
                        st.session_state["report_markdown"] = f"[Download Report]({download_url})"
                    else:
                        st.error(f"Failed to generate report: {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

    if "report_download_url" in st.session_state:
        st.markdown("### Generated Report")
        st.markdown(st.session_state["report_markdown"])



