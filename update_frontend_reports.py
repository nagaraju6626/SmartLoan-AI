import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the condition that checks target_path (we no longer care about it)
old_condition = '''        # 1. Validate dataset existence
        file_path_cleaned = os.path.join(PROCESSED_DIR, f"{dataset_id}_cleaned.csv")
        file_path_fallback = os.path.join(PROCESSED_DIR, f"{dataset_id}.csv")
        
        target_path = None
        if os.path.exists(file_path_cleaned):
            target_path = file_path_cleaned
        elif os.path.exists(file_path_fallback):
            target_path = file_path_fallback
            
        df = st.session_state.get('cleaned_df')
        if df is None:
            df = st.session_state.get('raw_df')
            
        if df is None:
            st.error("The active processed dataset could not be found. Please return to Data Upload and process the dataset again.")
        else:
            if len(df) == 0:
                st.error("The processed dataset is empty. Please process the dataset again.")
                df = None
                
        if target_path:
            with st.spinner("Generating report..."):
                try:'''

new_condition = '''        df = st.session_state.get('cleaned_df')
        if df is None:
            df = st.session_state.get('raw_df')
            
        if df is None or len(df) == 0:
            st.error("No dataset found. Please return to Data Upload and upload the file again.")
        else:
            with st.spinner("Generating report..."):
                try:'''

content = content.replace(old_condition, new_condition)

# 2. Update the payload and response handling
old_payload = '''                    payload = {
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
                    st.error(f"Error connecting to backend: {e}")'''

new_payload = '''                    payload = {
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
                        st.error(f"Report generation failed: {res.json().get('detail', 'Unknown Error')}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")'''

content = content.replace(old_payload, new_payload)

# 3. Update the download button rendering
old_download = '''    if st.session_state.get("report_markdown"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Your report is ready.")
        st.markdown(st.session_state["report_markdown"])'''

new_download = '''    if st.session_state.get("report_pdf_bytes"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Business Report",
            data=st.session_state["report_pdf_bytes"],
            file_name=f"smart_loan_business_report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )'''

content = content.replace(old_download, new_download)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
