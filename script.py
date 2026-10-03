import re
import io

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix dataset name truncation
old_metric = '    c1.metric("Dataset", dataset_name)'
new_metric = '''    with c1:
        st.markdown(f"<div style='margin-top: -5px;'><label style='font-size: 14px; color: rgb(49, 51, 63);'>Dataset</label><div title='{dataset_name}' style='font-size: 1.8rem; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%; color: rgb(49, 51, 63);'>{dataset_name}</div></div>", unsafe_allow_html=True)'''
content = content.replace(old_metric, new_metric)

# 2. Reduce vertical spacing
old_spacing1 = '''    st.markdown("---")

    # --------------------------------------------------
    # SELECT MODELS'''
new_spacing1 = '''    # --------------------------------------------------
    # SELECT MODELS'''
content = content.replace(old_spacing1, new_spacing1)

# 3. Active Model Section and State Reset
# Find the start of MODEL PERFORMANCE SUMMARY (Always show active status)
old_summary_start = '''    # --------------------------------------------------
    # MODEL PERFORMANCE SUMMARY (Always show active status)
    # --------------------------------------------------
    st.markdown("---")
    st.markdown("### 🏆 Model Performance Summary")
    
    active_ver = st.session_state.get('active_model_version', 'None')
    active_name = st.session_state.get('active_model_name', 'None')'''

new_summary_start = '''    # Validate active model against current training results
    active_ver = st.session_state.get('active_model_version')
    active_name = st.session_state.get('active_model_name')
    if success_results:
        current_valid_versions = [r["version"] for r in success_results]
        if active_ver not in current_valid_versions:
            st.session_state['active_model_version'] = None
            st.session_state['active_model_name'] = None
            active_ver = None
            active_name = None

    # --------------------------------------------------
    # MODEL PERFORMANCE SUMMARY (Always show active status)
    # --------------------------------------------------
    st.markdown("---")
    st.markdown("### 🏆 Model Performance Summary")'''
content = content.replace(old_summary_start, new_summary_start)

# In the summary logic, fix the 'None' check since it might be literally None now instead of 'None'
old_status_html_check = '''    if active_ver != 'None' and active_ver is not None:'''
new_status_html_check = '''    if active_ver:'''
content = content.replace(old_status_html_check, new_status_html_check)

# 4. Remove individual Set Active Model buttons
old_button = r'''        if st\.button\(f"Set \{alg\} as Active Model", key=f"active_\{r\['algorithm'\]\}_\{ver\}", type="primary"\):.*?st\.rerun\(\)\s*'''
content = re.sub(old_button, '', content, flags=re.DOTALL)

# 5. Insert separate Active Model Selection section before Model Comparison Summary
old_comp_summary_start = '''    # --------------------------------------------------
    # MODEL COMPARISON SUMMARY
    # --------------------------------------------------'''

new_comp_summary_start = '''    # --------------------------------------------------
    # ACTIVE MODEL SELECTION
    # --------------------------------------------------
    st.markdown("### 🎯 Active Model Selection")
    
    model_options = {f"{r['algorithm'].replace('_', ' ').title()} ({r['version']})": r for r in success_results}
    
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        selected_model_key = st.selectbox("Select a trained model:", list(model_options.keys()))
        
    with col_sel2:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Set Active Model", type="primary", use_container_width=True):
            r = model_options[selected_model_key]
            st.session_state['active_model_version'] = r["version"]
            st.session_state['active_model_name'] = r["algorithm"].replace('_', ' ').title()
            st.rerun()
            
    st.markdown("---")

    # --------------------------------------------------
    # MODEL COMPARISON SUMMARY
    # --------------------------------------------------'''
content = content.replace(old_comp_summary_start, new_comp_summary_start)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Edits complete.")
