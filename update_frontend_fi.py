import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the frontend feature importance computation
old_fi_block = r'''        with col_fi:
            st.markdown("\*\*Feature Importance / Influence\*\*")
            # Try to load model to extract importance
            model_path = os.path.join\(MODELS_DIR, f"model_{ver}\.pkl"\)
            if os\.path\.exists\(model_path\):
                try:
                    pipeline = joblib\.load\(model_path\)
                    classifier = pipeline\.named_steps\['classifier'\]
                    preprocessor = pipeline\.named_steps\['preprocessor'\]
                    
                    # Extract feature names
                    if hasattr\(preprocessor, 'get_feature_names_out'\):
                        feature_names = list\(preprocessor\.get_feature_names_out\(\)\)
                        # Clean up prefixes from ColumnTransformer \(e\.g\., 'num__', 'cat__'\)
                        feature_names = \[f\.split\("__", 1\)\[-1\] if "__" in f else f for f in feature_names\]
                    else:
                        num_features = r\.get\("features", \[\]\)
                        cat_features = \[\]
                        if hasattr\(preprocessor, 'transformers_'\):
                            for name, trans, cols in preprocessor\.transformers_:
                                if name == 'num': num_features = cols
                                if name == 'cat':
                                    try:
                                        cat_features = list\(trans\.get_feature_names_out\(cols\)\)
                                    except:
                                        cat_features = cols
                        feature_names = num_features \+ cat_features
                        
                    # Extract importances
                    importances = None
                    if hasattr\(classifier, 'feature_importances_'\):
                        importances = classifier\.feature_importances_
                    elif hasattr\(classifier, 'coef_'\):
                        importances = np\.abs\(classifier\.coef_\[0\]\)
                        
                    if importances is not None and len\(importances\) == len\(feature_names\):
                        fi_df = pd\.DataFrame\(\{"Feature": feature_names, "Importance": importances\}\)
                        fi_df = fi_df\.sort_values\(by="Importance", ascending=False\)\.head\(10\)
                        
                        fig_fi = px\.bar\(fi_df, x="Importance", y="Feature", orientation='h', color_discrete_sequence=\["#3B82F6"\]\)
                        fig_fi = apply_chart_style\(fig_fi\)
                        fig_fi\.update_layout\(margin=dict\(l=0, r=0, t=0, b=0\), height=250\)
                        fig_fi\.update_yaxes\(categoryorder="total ascending"\)
                        st\.plotly_chart\(fig_fi, use_container_width=True, key=f"feature_importance_{model_key}_{ver}"\)
                    else:
                        st\.info\("Feature importance is not available for this model\."\)
                except Exception as e:
                    st\.info\("Feature importance is not available for this model\."\)
            else:
                st\.info\("Model file not found locally to compute feature importance\."\)'''

new_fi_block = '''        with col_fi:
            st.markdown("**Feature Importance / Influence**")
            fi_data = r.get("feature_importance", [])
            
            if fi_data and len(fi_data) > 0:
                fi_df = pd.DataFrame(fi_data)
                
                # Format to percentage string for a clean table if we don't want a bar chart
                # But a bar chart is better as previously used
                fig_fi = px.bar(fi_df, x="importance", y="feature", orientation='h', color_discrete_sequence=["#3B82F6"])
                fig_fi = apply_chart_style(fig_fi)
                fig_fi.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250)
                fig_fi.update_yaxes(categoryorder="total ascending")
                fig_fi.update_traces(hovertemplate='%{y}: %{x:.1%}')
                fig_fi.update_xaxes(tickformat='.0%')
                
                st.plotly_chart(fig_fi, use_container_width=True, key=f"feature_importance_{model_key}_{ver}")
            else:
                st.info("Feature importance is not available for this model.")'''

content = re.sub(old_fi_block, new_fi_block, content, flags=re.DOTALL)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)
