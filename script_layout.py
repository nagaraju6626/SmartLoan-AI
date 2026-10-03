import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Subtitle
content = content.replace(
    'st.markdown("Train multiple machine learning models, evaluate their performance, and select an active model.")',
    'st.markdown("Train, evaluate, and activate machine learning models")'
)

# Dataset Configuration section
old_ds_config = '''    # --------------------------------------------------
    # DATASET & TRAINING CONFIGURATION
    # --------------------------------------------------
    st.markdown("### 📊 Dataset & Training Configuration")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        target_col = st.selectbox("Select Target Column", cols, index=default_idx)
        
    total_samples = len(df)
    train_samples = int(total_samples * 0.8)
    test_samples = total_samples - train_samples
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div style='margin-top: -5px;'><label style='font-size: 14px; color: rgb(49, 51, 63);'>Dataset</label><div title='{dataset_name}' style='font-size: 1.8rem; font-weight: 500; word-wrap: break-word; white-space: normal; line-height: 1.2; max-width: 100%; color: rgb(49, 51, 63);'>{dataset_name}</div></div>", unsafe_allow_html=True)
    c2.metric("Total Samples", f"{total_samples:,}")
    c3.metric("Features", f"{len(cols):,}")
    c4.metric("Train/Test Split", "80% / 20%")'''

new_ds_config = '''    # --------------------------------------------------
    # DATASET CONFIGURATION
    # --------------------------------------------------
    st.markdown("### Dataset Configuration")
    
    total_samples = len(df)
    
    config_card = f"""
    <div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 20px;'>
        <p style='margin-bottom: 10px; font-size: 16px;'><b>Dataset:</b> <span style='word-wrap: break-word; color: #334155;'>{dataset_name}</span></p>
        <p style='margin-bottom: 0; font-size: 16px;'>
            <b>Samples:</b> <span style='color: #334155;'>{total_samples:,}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>Features:</b> <span style='color: #334155;'>{len(cols):,}</span> &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>Split:</b> <span style='color: #334155;'>80/20</span>
        </p>
    </div>
    """
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        target_col = st.selectbox("Target Column", cols, index=default_idx)
        
    st.markdown(config_card, unsafe_allow_html=True)'''

content = content.replace(old_ds_config, new_ds_config)

# Training Readiness
old_readiness = '''    # --------------------------------------------------
    # TRAINING READINESS
    # --------------------------------------------------
    st.markdown("### ✅ Training Readiness")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("✓ Dataset loaded")
        if target_col in cols:
            st.markdown("✓ Target column detected")
        else:
            st.markdown("❌ Missing target column")
        num_feats = df.select_dtypes(include=[np.number]).columns.tolist()
        cat_feats = df.select_dtypes(exclude=[np.number]).columns.tolist()
        st.markdown(f"✓ {len(num_feats)} numerical & {len(cat_feats)} categorical features detected")
    with r2:
        if df.isnull().sum().sum() == 0:
            st.markdown("✓ Missing values checked")
        else:
            st.markdown("⚠️ Missing values present (will be imputed)")
        st.markdown("✓ Preprocessing configured")
        st.markdown("✓ Train/Test split ready")'''

new_readiness = '''    # --------------------------------------------------
    # TRAINING READINESS
    # --------------------------------------------------
    st.markdown("### Training Readiness")
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("✓ Dataset loaded")
        if target_col in cols:
            st.markdown("✓ Target detected")
        else:
            st.markdown("❌ Missing target")
        st.markdown("✓ Features detected")
    with r2:
        if df.isnull().sum().sum() == 0:
            st.markdown("✓ Missing values checked")
        else:
            st.markdown("⚠️ Missing values present")
        st.markdown("✓ Preprocessing configured")
        st.markdown("✓ Train/Test split ready")'''

content = content.replace(old_readiness, new_readiness)

# Models to Train
old_models = '''    # --------------------------------------------------
    # SELECT MODELS
    # --------------------------------------------------
    st.markdown("### 🧠 Select Models")'''

new_models = '''    # --------------------------------------------------
    # MODELS TO TRAIN
    # --------------------------------------------------
    st.markdown("### Models to Train")'''

content = content.replace(old_models, new_models)

# Center the Start Training button
old_button = '''    if st.button("Start Training", type="primary"):'''
new_button = '''    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, c_btn3 = st.columns([1, 2, 1])
    with c_btn2:
        start_btn = st.button("Start Training", type="primary", use_container_width=True)
        
    if start_btn:'''

content = content.replace(old_button, new_button)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Edits complete.")
