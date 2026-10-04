import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add warning for partially failed models
old_display = '''    if not success_results:
        st.error("All selected models failed to train.")
        for r in results:
            st.error(f"{r['algorithm']}: {r['error']}")
        return'''

new_display = '''    if not success_results:
        st.error("All selected models failed to train.")
        for r in results:
            st.error(f"{r['algorithm']}: {r['error']}")
        return
        
    failed_results = [r for r in results if "error" in r]
    if failed_results:
        for r in failed_results:
            st.warning(f"Failed to train {r['algorithm']}: {r['error']}")'''

content = content.replace(old_display, new_display)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)
