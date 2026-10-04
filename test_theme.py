import pandas as pd
import streamlit as st

def apply_dataframe_style(df):
    if not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except Exception:
            pass
            
    if isinstance(df, pd.DataFrame):
        theme = st.session_state.get("theme", "light")
        if theme == "dark":
            return df.style.set_properties(**{
                'background-color': '#1E293B',
                'color': '#F1F5F9',
                'border-color': '#334155'
            }).set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#0F172A'), 
                    ('color', '#F1F5F9'),
                    ('border-color', '#334155')
                ]},
                {'selector': 'td', 'props': [
                    ('border-color', '#334155')
                ]}
            ])
    return df
