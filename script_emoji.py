import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix mangled emojis
content = re.sub(r'st\.markdown\("###.*?Dataset & Training Configuration"\)', 'st.markdown("### 📊 Dataset & Training Configuration")', content)
content = re.sub(r'st\.markdown\("###.*?Training Readiness"\)', 'st.markdown("### ✅ Training Readiness")', content)
content = re.sub(r'st\.markdown\("###.*?Select Models"\)', 'st.markdown("### 🧠 Select Models")', content)
content = re.sub(r'st\.markdown\("###.*?Active Model Selection"\)', 'st.markdown("### 🎯 Active Model Selection")', content)
content = re.sub(r'st\.markdown\("###.*?Model Performance Summary"\)', 'st.markdown("### 🏆 Model Performance Summary")', content)
content = re.sub(r'st\.markdown\("###.*?Model Comparison"\)', 'st.markdown("### ⚖️ Model Comparison")', content)
content = re.sub(r'st\.markdown\("###.*?Individual Model Results"\)', 'st.markdown("### 🔍 Individual Model Results")', content)

content = re.sub(r'st\.markdown\(".*?Dataset loaded"\)', 'st.markdown("✓ Dataset loaded")', content)
content = re.sub(r'st\.markdown\(".*?Target column detected"\)', 'st.markdown("✓ Target column detected")', content)
content = re.sub(r'st\.markdown\(".*?Missing target column"\)', 'st.markdown("❌ Missing target column")', content)
content = re.sub(r'st\.markdown\(".*?Missing values checked"\)', 'st.markdown("✓ Missing values checked")', content)
content = re.sub(r'st\.markdown\(".*?Missing values present.*?imputed\)"\)', 'st.markdown("⚠️ Missing values present (will be imputed)")', content)
content = re.sub(r'st\.markdown\(".*?Preprocessing configured"\)', 'st.markdown("✓ Preprocessing configured")', content)
content = re.sub(r'st\.markdown\(".*?Train/Test split ready"\)', 'st.markdown("✓ Train/Test split ready")', content)

content = re.sub(r'st\.markdown\(f".*?\{len\(num_feats\)\}.*?numerical &.*?\{len\(cat_feats\)\}.*?categorical features detected"\)', 'st.markdown(f"✓ {len(num_feats)} numerical & {len(cat_feats)} categorical features detected")', content)

content = re.sub(r'"Status": ".*?Failed"', '"Status": "❌ Failed"', content)
content = re.sub(r'"Status": ".*?Success"', '"Status": "✅ Success"', content)
content = re.sub(r'"Status": ".*?Success \(Active\)"', '"Status": "✅ Success (Active)"', content)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Emojis fixed.")
