import re

with open("frontend/components/theme.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove initialize_theme and toggle_theme functions
pattern = re.compile(r'def initialize_theme\(\):.*?def apply_theme\(\):', re.DOTALL)
content = pattern.sub('def apply_theme():', content)

# Remove initialize_theme() and theme = st.session_state.theme from apply_theme()
content = content.replace('    initialize_theme()\n', '')
content = content.replace('    theme = st.session_state.theme\n', '    theme = "light"\n')

# Remove the dark CSS block in apply_theme:
# It's inside `if theme == "light": ... else: dark_css = ...`
# Let's just find the `else:` block and remove it. We'll use a regex that matches `    else:\n        dark_css = """\n        <style>\n.*?        """\n        st.markdown\(dark_css, unsafe_allow_html=True\)`
dark_css_pattern = re.compile(r'    else:\n        dark_css = """.*?        st\.markdown\(dark_css, unsafe_allow_html=True\)', re.DOTALL)
content = dark_css_pattern.sub('', content)

# We can also just remove the `if theme == "light":` and unindent the light_css, but keeping the `if theme == "light":` is fine if `theme = "light"` is hardcoded.

# In apply_chart_style(fig):
content = content.replace('    theme = st.session_state.get("theme", "light")\n', '    theme = "light"\n')

# In apply_dataframe_style(df):
content = content.replace('        theme = st.session_state.get("theme", "light")\n', '        theme = "light"\n')

with open("frontend/components/theme.py", "w", encoding="utf-8") as f:
    f.write(content)
