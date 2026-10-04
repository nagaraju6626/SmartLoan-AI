import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_run = 'uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)'
new_run = 'port = int(os.environ.get("PORT", 8000))\n    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)'

content = content.replace(old_run, new_run)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
