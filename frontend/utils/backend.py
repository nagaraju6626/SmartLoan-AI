import time
import httpx
import streamlit as st

def wait_for_backend(api_base_url: str, max_retries: int = 15, wait_seconds: int = 5) -> bool:
    """
    Checks if the backend is awake (Render cold starts can take 50+ seconds).
    Retries multiple times before giving up.
    """
    health_url = f"{api_base_url.rstrip('/')}/api/health"
    status_placeholder = st.empty()
    
    for attempt in range(max_retries):
        try:
            res = httpx.get(health_url, timeout=10.0)
            if res.status_code == 200:
                status_placeholder.empty()
                return True
        except (httpx.TimeoutException, httpx.RequestError):
            pass
        
        status_placeholder.info(f"Backend is starting up, please wait... (Attempt {attempt + 1}/{max_retries})")
        time.sleep(wait_seconds)
        
    status_placeholder.empty()
    return False
