import re

with open("frontend/components/navigation.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove GLOBAL THEME STATE block
pattern = re.compile(r'    # ----------------------------------------\n    # GLOBAL THEME STATE\n    # ----------------------------------------\n    if "theme" not in st\.session_state:\n        st\.session_state\["theme"\] = "light"\n        \n', re.DOTALL)
content = pattern.sub('', content)

content = content.replace('    theme = st.session_state["theme"]\n', '')

# Replace the fallback for CSS
pattern2 = re.compile(r'    # Provide safe fallback for CSS just in case\n    if theme == "dark":.*?    else:\n        css = f"""<style>\n        /\* LIGHT MODE SIDEBAR SPECIFIC OVERRIDES IF NEEDED \*/\n        \[data-testid="stSidebar"\] \{\{\n            background-color: #0B1930 !important;\n        \}\}\n        """\n', re.DOTALL)

replacement = '''    # Provide safe fallback for CSS just in case
    css = f"""<style>
    /* LIGHT MODE SIDEBAR SPECIFIC OVERRIDES IF NEEDED */
    [data-testid="stSidebar"] {{
        background-color: #0B1930 !important;
    }}
    """
'''
content = pattern2.sub(replacement, content)

with open("frontend/components/navigation.py", "w", encoding="utf-8") as f:
    f.write(content)
