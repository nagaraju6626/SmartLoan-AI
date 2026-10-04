import subprocess
import time
import sys

print('Starting Streamlit...')
p = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'frontend/app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

start_time = time.time()
while time.time() - start_time < 10:
    ret = p.poll()
    if ret is not None:
        print(f'Streamlit crashed with code {ret}!')
        out, err = p.communicate()
        print('STDOUT:')
        print(out)
        print('STDERR:')
        print(err)
        sys.exit(1)
    time.sleep(0.5)

print('Streamlit is still running after 10 seconds. It did not crash.')
p.terminate()
