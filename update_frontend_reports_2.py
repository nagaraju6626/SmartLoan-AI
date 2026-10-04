import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

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
                        st.error(f"Report generation failed: {res.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")'''

# Use regex spacing tolerance just in case
content = re.sub(
    r'payload = \{.*?"prediction_inputs": prediction_inputs\s*\}.*?res = httpx\.post.*?except Exception as e:\s*st\.error.*?backend:.*?\}',
    new_payload.replace('\n', '\\n').replace('"', '\\"'),
    content,
    flags=re.DOTALL
)

# Better: just use simple regex for payload to the except block
pattern = r'payload = \{.*?"prediction_inputs": prediction_inputs\s*\}.*?res = httpx\.post.*?except Exception as e:\s*st\.error[^\n]*'
content = re.sub(pattern, new_payload, content, flags=re.DOTALL)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
