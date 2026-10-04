import streamlit as st
import pandas as pd

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
st.dataframe(df)

styled = df.style.set_properties(**{'background-color': '#1E293B', 'color': '#F1F5F9', 'border-color': '#334155'})
styled = styled.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#0F172A'), ('color', '#F1F5F9')]}
])
st.dataframe(styled)
