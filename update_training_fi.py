import re

with open('backend/ml/training.py', 'r', encoding='utf-8') as f:
    content = f.read()

fi_code = '''    # Extract feature importance
    feature_importance_list = []
    try:
        classifier_step = pipeline.named_steps['classifier']
        preprocessor_step = pipeline.named_steps['preprocessor']
        
        if hasattr(preprocessor_step, 'get_feature_names_out'):
            feature_names = list(preprocessor_step.get_feature_names_out())
            feature_names = [f.split("__", 1)[-1] if "__" in f else f for f in feature_names]
        else:
            feature_names = numeric_features + categorical_features
            
        importances = None
        if hasattr(classifier_step, 'feature_importances_'):
            importances = classifier_step.feature_importances_
        elif hasattr(classifier_step, 'coef_'):
            importances = np.abs(classifier_step.coef_[0])
            
        if importances is not None and len(importances) == len(feature_names):
            total = np.sum(importances)
            if total > 0:
                importances = importances / total
                
            fi_data = [{"feature": f, "importance": float(i)} for f, i in zip(feature_names, importances)]
            feature_importance_list = sorted(fi_data, key=lambda x: x["importance"], reverse=True)[:10]
    except Exception:
        pass
        
'''

# Insert before metadata dict
pattern = r'(\s*metadata = \{\s*"version": version,)'
replacement = fi_code + r'\1'
content = re.sub(pattern, replacement, content)

# Add "feature_importance": feature_importance_list to metadata
meta_pattern = r'("metrics": metrics,)'
meta_replacement = r'\1\n        "feature_importance": feature_importance_list,'
content = re.sub(meta_pattern, meta_replacement, content)

with open('backend/ml/training.py', 'w', encoding='utf-8') as f:
    f.write(content)
