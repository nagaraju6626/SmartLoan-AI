import streamlit as st
from frontend.components.theme import apply_dataframe_style
import httpx
import pandas as pd
import os
from dotenv import load_dotenv

import sys
from pathlib import Path

# Ensure we always load .env from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Data Upload", page_icon="??", layout="wide")

from frontend.components.navigation import render_sidebar
from frontend.components.header import render_header

# --- Authentication Check ---
if not st.session_state.get("authenticated", False):
    st.switch_page("pages/00_Login.py")
# ----------------------------

render_sidebar()
render_header()

st.title("Data Upload")
st.markdown("Upload your historical loan dataset (CSV) to begin analysis.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    if st.button("Upload Dataset"):
        with st.spinner("Uploading and analyzing dataset..."):
            try:
                # Increased timeout to 10s just in case backend is slow to respond initially
                health_res = httpx.get(f"{API_BASE_URL}/api/health", timeout=10.0)
                if health_res.status_code != 200:
                    st.error(f"Backend server returned an error: {health_res.status_code}. Please check backend logs.")
                    st.stop()
            except httpx.ConnectError:
                st.error(f"Backend server is not running at {API_BASE_URL}. Please start the backend and try again.")
                st.stop()
            except httpx.TimeoutException:
                st.error("Backend server timed out during health check. Please ensure it's responding.")
                st.stop()
            except httpx.RequestError as e:
                st.error(f"Backend request failed: {str(e)}")
                st.stop()
            
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                # Increased timeout for large files
                response = httpx.post(f"{API_BASE_URL}/api/upload", files=files, timeout=120.0)
                
                if response.status_code == 200:
                    data_info = response.json()
                    dataset_id = data_info['id']
                    
                    st.session_state['current_dataset_id'] = dataset_id
                    st.session_state['current_dataset_name'] = data_info['filename']
                    
                    st.success(f"Successfully uploaded {data_info['filename']}!")
                    
                    # Also fetch the full analysis (can take time for large datasets)
                    analysis_res = httpx.get(f"{API_BASE_URL}/api/analysis/{dataset_id}", timeout=120.0)
                    if analysis_res.status_code == 200:
                        analysis = analysis_res.json()
                        st.session_state['dataset_analysis'] = analysis
                        
                else:
                    st.error(f"Error uploading file: {response.json().get('detail', 'Unknown error')}")
            except httpx.ConnectError:
                st.error("Lost connection to the backend server during upload.")
            except httpx.TimeoutException:
                st.error("The backend server timed out while processing the dataset. Please try a smaller file or check backend logs.")
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")

st.markdown("---")

if 'dataset_analysis' in st.session_state:
    analysis = st.session_state['dataset_analysis']
    
    st.markdown("### Dataset Quality Information")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", analysis["total_rows"])
    col2.metric("Columns", analysis["total_columns"])
    col3.metric("Duplicate Rows", analysis["duplicate_rows"])
    col4.metric("Total Missing", sum(analysis["missing_values"].values()))
    
    st.markdown("#### Detected Columns")
    mapping = analysis["detected_mapping"]
    
    target_col = mapping.get("target", "Not Found")
    st.info(f"?? **Possible Target Column:** {target_col}")
    
    # Missing values and data types
    st.markdown("#### Column Details (Missing & Types)")
    missing = analysis["missing_values"]
    dtypes = analysis.get("data_types", {})
    col_details = []
    for col in analysis.get("columns", []):
        col_details.append({
            "Column": col,
            "Missing Values": missing.get(col, 0),
            "Data Type": dtypes.get(col, "unknown")
        })
    st.dataframe(apply_dataframe_style(pd.DataFrame(col_details)), use_container_width=True, hide_index=True)
    
    st.markdown("### Data Preview")
    try:
        preview_res = httpx.get(f"{API_BASE_URL}/api/datasets/{st.session_state['current_dataset_id']}", timeout=30.0)
        if preview_res.status_code == 200:
            preview_data = preview_res.json()
            if not preview_data:
                st.info("No data available for preview.")
            else:
                df_preview = pd.DataFrame(preview_data)
                total_rows = analysis.get("total_rows", len(df_preview))
                displayed_rows = len(df_preview)
                st.caption(f"Showing first {displayed_rows} of {total_rows} rows")
                st.dataframe(apply_dataframe_style(df_preview), use_container_width=True)
        else:
            st.error(f"Unable to load dataset preview. Error {preview_res.status_code}")
    except httpx.ConnectError:
        st.error("Lost connection to the backend server while fetching preview.")
    except httpx.TimeoutException:
        st.error("Backend server timed out while fetching preview.")
    except Exception as e:
        st.error(f"Unable to load dataset preview. Connection error: {str(e)}")
