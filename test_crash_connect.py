import subprocess
import time
import sys
import urllib.request

print('Starting Streamlit...')
p = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'frontend/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

time.sleep(3) # Wait for startup

try:
    print('Connecting to Streamlit...')
    req = urllib.request.Request('http://localhost:8501')
    response = urllib.request.urlopen(req, timeout=5)
    print('Response status:', response.status)
except Exception as e:
    print('Error connecting:', e)

time.sleep(3)
ret = p.poll()
if ret is not None:
    print(f'Streamlit crashed with code {ret}!')
    out, err = p.communicate()
    print('STDOUT:')
    print(out)
    print('STDERR:')
    print(err)
else:
    print('Streamlit is still running.')
    p.terminate()
