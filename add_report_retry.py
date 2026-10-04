import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

helper = '''
import time
import httpx

def wait_for_backend(api_base_url):
    status_placeholder = st.empty()
    max_retries = 20
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            res = httpx.get(f"{api_base_url}/api/health", timeout=10.0)
            if res.status_code == 200:
                status_placeholder.empty()
                return True
        except (httpx.ConnectError, httpx.TimeoutException, httpx.RequestError):
            pass
            
        status_placeholder.info("Starting backend server... Render may take up to a minute on the first request.")
        time.sleep(retry_delay)
        
    status_placeholder.empty()
    return False
'''

# Add the helper at the top, right before main()
pattern_insert = r'def main\(\):'
content = re.sub(pattern_insert, helper + '\ndef main():', content)

# Use the helper before the API call
old_spinner = '''            with st.spinner("Generating report..."):
                try:'''

new_spinner = '''            if not wait_for_backend(API_BASE_URL):
                st.error("Backend is taking too long to start. Please try again in a moment.")
                st.stop()
                
            with st.spinner("Generating report..."):
                try:'''

content = content.replace(old_spinner, new_spinner)

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
