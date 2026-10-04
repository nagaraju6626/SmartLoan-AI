import urllib.request
import json
import time
import subprocess

p = subprocess.Popen(['venv\\Scripts\\python.exe', '-m', 'streamlit', 'run', 'frontend\\app.py'])
time.sleep(4)

try:
    req = urllib.request.Request('http://localhost:8501/_stcore/health')
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print('Error:', e)

p.terminate()
