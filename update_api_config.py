import os
import glob
import re

files = glob.glob('frontend/**/*.py', recursive=True)

# 1. Update Error Messages
old_error_pattern = r'st\.error\(f"Backend server is not running at \{API_BASE_URL\}\. Please start the backend and try again\."\)'
new_error = 'st.error("Unable to connect to the backend server. Please try again later. (In local dev, ensure FastAPI is running on port 8000)")'

# 2. Make sure API_BASE_URL uses st.secrets as well just in case they use nested secrets
old_api_def = r'API_BASE_URL = os\.getenv\("API_BASE_URL", "http://127\.0\.0\.1:8000"\)'
new_api_def = '''try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://127.0.0.1:8000"))
except Exception:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")'''

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = False
    
    if re.search(old_error_pattern, content):
        content = re.sub(old_error_pattern, new_error, content)
        updated = True
        
    if re.search(old_api_def, content):
        content = re.sub(old_api_def, new_api_def, content)
        updated = True
        
    if updated:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
