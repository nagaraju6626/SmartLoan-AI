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
from frontend.utils.backend import wait_for_backend

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

def get_active_dataset():
    if 'cleaned_df' in st.session_state or 'raw_df' in st.session_state:
        ds_id = st.session_state.get('processed_dataset_id', st.session_state.get('current_dataset_id'))
        ds_name = st.session_state.get('processed_dataset_name', st.session_state.get('current_dataset_name', 'Unknown'))
        return ds_id, ds_name
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
        df = st.session_state.get('cleaned_df')
        if df is None:
            df = st.session_state.get('raw_df')
            
        if df is None or len(df) == 0:
            st.error("No dataset found. Please return to Data Upload and upload the file again.")
        else:
            if not wait_for_backend(API_BASE_URL):
                st.error("Backend is taking too long to start. Please try again in a moment.")
                st.stop()
                
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
                        "prediction_inputs": prediction_inputs,
                        "csv_data": df.to_csv(index=False)
                    }
                    res = httpx.post(f"{API_BASE_URL}/api/reports/generate", json=payload, timeout=90.0)
                    if res.status_code == 200:
                        st.success("Business report generated successfully.")
                        st.session_state["report_pdf_bytes"] = res.content
                    else:
                        st.error(f"Report generation failed: {res.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

    if st.session_state.get("report_pdf_bytes"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Business Report",
            data=st.session_state["report_pdf_bytes"],
            file_name=f"smart_loan_business_report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )



