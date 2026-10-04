import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the success message to check for at least one successful model
old_success = '''                    if train_res.status_code == 200:
                        st.session_state["training_results"] = train_res.json()["results"]
                        st.success("Training completed successfully!")'''

new_success = '''                    if train_res.status_code == 200:
                        train_results = train_res.json()["results"]
                        st.session_state["training_results"] = train_results
                        if any("error" not in r for r in train_results):
                            st.success("Training completed successfully!")
                        else:
                            st.error("All selected models failed to train.")'''

content = content.replace(old_success, new_success)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)
