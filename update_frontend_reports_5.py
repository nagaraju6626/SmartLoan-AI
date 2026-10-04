import re

with open('frontend/pages/10_Reports.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('                                        payload = {', '                    payload = {')

with open('frontend/pages/10_Reports.py', 'w', encoding='utf-8') as f:
    f.write(content)
