import re

with open('frontend/pages/05_Model_Training.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'# Try to load model to extract importance.*?st\.info\("Model file not found locally to compute feature importance\."\)'

new_fi_block = '''fi_data = r.get("feature_importance", [])
            
            if fi_data and len(fi_data) > 0:
                fi_df = pd.DataFrame(fi_data)
                
                fig_fi = px.bar(fi_df, x="importance", y="feature", orientation='h', color_discrete_sequence=["#3B82F6"])
                fig_fi = apply_chart_style(fig_fi)
                fig_fi.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250)
                fig_fi.update_yaxes(categoryorder="total ascending")
                fig_fi.update_traces(hovertemplate='%{y}: %{x:.1%}')
                fig_fi.update_xaxes(tickformat='.0%')
                
                st.plotly_chart(fig_fi, use_container_width=True, key=f"feature_importance_{model_key}_{ver}")
            else:
                st.info("Feature importance is not available for this model.")'''

content = re.sub(pattern, new_fi_block, content, flags=re.DOTALL)

with open('frontend/pages/05_Model_Training.py', 'w', encoding='utf-8') as f:
    f.write(content)
