
import streamlit as st

def apply_css():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #111315;
        color: #f5f5f5;
        font-family: Arial, sans-serif;
    }

    /* Main content */
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #ff922b !important;
        font-weight: 700 !important;
    }

    /* Normal text and labels */
    p, label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] * {
        color: #eeeeee !important;
        opacity: 1 !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        background-color: #1b1d20 !important;
        color: #eeeeee !important;
        opacity: 1 !important;
        border-radius: 6px 6px 0 0 !important;
    }

    button[data-baseweb="tab"] * {
        color: #eeeeee !important;
    }

    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] * {
        color: #ff922b !important;
        font-weight: 700 !important;
    }
    div[data-testid="stNumberInput"] button {
    display: none !important;
    }
    /* Input fields */
    [data-testid="stNumberInput"] input {
        background-color: #242629 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #555555 !important;
    }
    div[data-testid="stNumberInput"] button {
    display: none !important;
    }
    [data-baseweb="select"] > div {
        background-color: #242629 !important;
        border: 1px solid #555555 !important;
    }

    [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* Form and metric cards */
    [data-testid="stForm"],
    [data-testid="stMetric"] {
        background-color: #1b1d20 !important;
        border: 1px solid #663b1d !important;
        border-radius: 10px !important;
        padding: 18px !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #cccccc !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #ff922b !important;
    }

    /* Buttons */
    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        background-color: #ff922b !important;
        color: #151515 !important;
        border: 1px solid #ff922b !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }

    /* History expanders */
    [data-testid="stExpander"] {
        background-color: #1b1d20 !important;
        border: 1px solid #663b1d !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: #eeeeee !important;
    }

    /* Captions */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #b8b8b8 !important;
    }

    /* No transitions or hover styling */
    *, *::before, *::after {
        transition: none !important;
        animation: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
