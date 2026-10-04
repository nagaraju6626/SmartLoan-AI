import streamlit as st

def apply_theme():
    theme = "light"
    
    # Base CSS that applies to the theme (structural, shadows, radiuses)
    base_css = """
    <style>
    /* Search Bar Base Styling */
    div[data-testid="stTextInput"] > div > div > input {
        border-radius: 20px !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    
    /* Buttons Base Styling */
    div[data-testid="column"] > div > div > div > div > button {
        height: 44px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
        height: 44px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06) !important;
    }
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)
    
    if theme == "light":
        light_css = """
        <style>
        :root {
            --primary-color: #2563EB !important;
            --background-color: #F8FAFC !important;
            --secondary-background-color: #FFFFFF !important;
            --text-color: #0F172A !important;
        }
        .stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
        
        /* Search Bar & Header Controls (Light) */
        div[data-testid="stTextInput"] > div > div > input {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        div[data-testid="stTextInput"] > div > div > input::placeholder {
            color: #64748B !important;
        }
        div[data-testid="column"] > div > div > div > div > button {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #334155 !important;
        }
        div[data-testid="column"] > div > div > div > div[data-testid="stPopover"] > button {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #1E293B !important;
        }
        
        /* Force Hamburger Toggle Icon Visibility in ALL states */
        div[data-testid="column"]:nth-of-type(1) button p,
        div[data-testid="column"]:nth-of-type(1) button span,
        div[data-testid="column"]:nth-of-type(1) button svg {
            color: #334155 !important;
            fill: #334155 !important;
            stroke: #334155 !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
            text-indent: 0 !important;
        }
        </style>
        """
        st.markdown(light_css, unsafe_allow_html=True)


def apply_chart_style(fig):
    theme = "light"
    if theme == "dark":
        fig.update_layout(
            plot_bgcolor="#0F172A",
            paper_bgcolor="#0F172A",
            margin=dict(t=40, l=20, r=20, b=20),
            font=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9", size=16),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=False, linecolor="#334155", gridcolor="#334155")
        fig.update_yaxes(showgrid=True, gridcolor="#1E293B", linecolor="#334155")
    else:
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=40, l=20, r=20, b=20),
            font=dict(color="#334155"),
            title_font=dict(color="#0F172A", size=16),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=False, linecolor="#E2E8F0", gridcolor="#E2E8F0")
        fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", linecolor="#E2E8F0")
    return fig

import pandas as pd

def apply_dataframe_style(df):
    if not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except Exception:
            pass
            
    if isinstance(df, pd.DataFrame):
        theme = "light"
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
