import streamlit as st
import httpx
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header
render_sidebar()
render_header()


st.title("Business Reports")
st.markdown("Generate and download comprehensive reports for loan applications.")

if 'current_dataset_id' not in st.session_state:
    st.warning("Please upload a dataset first.")
else:
    dataset_id = st.session_state['current_dataset_id']
    st.info(f"Generating reports for dataset: {st.session_state['current_dataset_name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Report Type:** Business Report")
        report_type = "business_report"
    with col2:
        report_format = st.selectbox("Format", ["pdf"])
        
    if st.button("Generate Report"):
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
                    
                    st.markdown(f"[📥 Download Report]({download_url})")
                else:
                    st.error(f"Failed to generate report: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

