import re

with open('backend/ml/training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add encode_loan_status helper
helper_code = '''def encode_loan_status(y):
    mapping = {
        "Rejected": 0,
        "Approved": 1
    }
    encoded = y.map(mapping)
    if encoded.isna().any():
        invalid = y[encoded.isna()].unique().tolist()
        raise ValueError(f"Invalid Loan_Status values: {invalid}. Expected 'Approved' or 'Rejected'.")
    
    reverse_mapping = {0: "Rejected", 1: "Approved"}
    return encoded.astype(int), reverse_mapping

'''

# Find def train_model
content = content.replace('def train_model(', helper_code + 'def train_model(')

# Replace the existing encoding block
old_encoding_block = '''    # If target is categorical strings, encode to 0/1
    # Very basic encoding for binary classification
    target_mapping = None
    if y.dtype == 'object' or y.dtype.name == 'category':
        classes = y.unique()
        if len(classes) == 2:
            # Try to infer positive class
            pos_class = classes[0]
            for c in classes:
                if str(c).lower() in ['y', 'yes', 'approved', '1', 'true']:
                    pos_class = c
                    break
            y = (y == pos_class).astype(int)
            target_mapping = {int(1): str(pos_class), int(0): str([c for c in classes if c != pos_class][0])}
        else:
            raise ValueError("Only binary classification is currently supported.")'''

new_encoding_block = '''    # Ensure target is cleanly encoded
    y, target_mapping = encode_loan_status(y)
    
    if y.nunique() < 2:
        raise ValueError("Training requires both Approved and Rejected loan records.")'''

content = content.replace(old_encoding_block, new_encoding_block)

# Ensure stratified train/test split
old_split = "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"
new_split = "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)"
content = content.replace(old_split, new_split)

with open('backend/ml/training.py', 'w', encoding='utf-8') as f:
    f.write(content)
