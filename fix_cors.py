import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_cors = '''# Configure CORS
origins = [
    "http://localhost:8501", 
    "http://127.0.0.1:8501",
    "https://smartloan-approval-nr.streamlit.app"
]

# Allow additional origins via environment variable
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)'''

# Regex to replace the CORS middleware block
pattern = r'# Configure CORS\napp\.add_middleware\(\n\s*CORSMiddleware,\n\s*allow_origins=\[.*?\],\s*#.*?\n\s*allow_credentials=True,\n\s*allow_methods=\[".*?"\],\n\s*allow_headers=\[".*?"\],\n\)'

content = re.sub(pattern, new_cors, content, flags=re.DOTALL)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
