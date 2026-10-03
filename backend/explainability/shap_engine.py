import shap
import joblib
import pandas as pd
import numpy as np
import os

MODELS_DIR = "models/versions"

def generate_shap_explanation(model_version: str, input_data: pd.DataFrame):
    """
    Generate SHAP values for a specific prediction.
    Since we use a Pipeline with ColumnTransformer, extracting SHAP is complex.
    We will extract the preprocessor and the classifier.
    """
    model_path = os.path.join(MODELS_DIR, f"model_{model_version}.pkl")
    if not os.path.exists(model_path):
        raise ValueError(f"Model {model_version} not found.")
        
    pipeline = joblib.load(model_path)
    
    preprocessor = pipeline.named_steps['preprocessor']
    classifier = pipeline.named_steps['classifier']
    
    # Preprocess the data
    X_transformed = preprocessor.transform(input_data)
    
    # Get feature names after transformation
    feature_names = []
    
    # Extract feature names if possible
    try:
        # For numeric features, they stay the same
        num_features = preprocessor.transformers_[0][2]
        feature_names.extend(num_features)
        
        # For categorical features, get one-hot encoded names
        cat_features = preprocessor.transformers_[1][2]
        onehot_encoder = preprocessor.transformers_[1][1].named_steps['onehot']
        cat_encoded_names = onehot_encoder.get_feature_names_out(cat_features)
        feature_names.extend(cat_encoded_names)
    except Exception:
        # Fallback if extraction fails
        feature_names = [f"Feature_{i}" for i in range(X_transformed.shape[1])]
        
    # Extract feature values for the applicant
    if hasattr(X_transformed, 'toarray'):
        X_arr = X_transformed.toarray()[0]
    elif isinstance(X_transformed, np.ndarray):
        X_arr = X_transformed[0]
    else:
        X_arr = np.zeros(len(feature_names))
        
    model_type = type(classifier).__name__
    shap_values_to_plot = np.zeros(len(feature_names))
    base_value = 0.0
    
    if model_type == 'LogisticRegression' or hasattr(classifier, 'coef_'):
        # Explicitly calculate contribution = value * coefficient
        coefs = classifier.coef_[0]
        for i in range(len(feature_names)):
            if i < len(coefs):
                shap_values_to_plot[i] = float(X_arr[i]) * float(coefs[i])
        base_value = float(classifier.intercept_[0]) if hasattr(classifier, 'intercept_') else 0.0
    elif model_type in ['RandomForestClassifier', 'XGBClassifier', 'DecisionTreeClassifier']:
        try:
            # TreeExplainer does not require a background dataset by default
            explainer = shap.TreeExplainer(classifier)
            shap_values = explainer.shap_values(X_transformed)
            # Handle list output for classification
            if isinstance(shap_values, list):
                shap_values_to_plot = shap_values[1][0]
                base_value = explainer.expected_value[1] if isinstance(explainer.expected_value, (list, np.ndarray)) else explainer.expected_value
            else:
                shap_values_to_plot = shap_values[0]
                base_value = explainer.expected_value
        except Exception:
            # Fallback to feature_importances_ if SHAP fails for trees
            if hasattr(classifier, 'feature_importances_'):
                shap_values_to_plot = classifier.feature_importances_
    else:
        # Fallback for unsupported models
        if hasattr(classifier, 'feature_importances_'):
            shap_values_to_plot = classifier.feature_importances_
        
    # Create the waterfall/bar plot data
    # We will return the values so the frontend can plot them using plotly
    
    explanation = []
    for i, name in enumerate(feature_names):
        explanation.append({
            "feature": name,
            "value": float(X_transformed[0][i]) if isinstance(X_transformed, np.ndarray) else float(X_transformed.toarray()[0][i]) if hasattr(X_transformed, 'toarray') else 0.0,
            "shap_value": float(shap_values_to_plot[i])
        })
        
    # Sort by absolute shap value
    explanation = sorted(explanation, key=lambda x: abs(x["shap_value"]), reverse=True)
    
    return {
        "base_value": float(base_value) if isinstance(base_value, (float, int, np.float32, np.float64)) else float(base_value[0]),
        "features": explanation
    }
