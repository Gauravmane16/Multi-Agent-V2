"""
Main application file for the Code Assistant App.
"""

import streamlit as st
from dotenv import load_dotenv
from components.sidebar import render_sidebar
from components.optimizer_tab import render_optimizer_tab
from components.reviewer_tab import render_reviewer_tab
from components.comparer_tab import render_comparer_tab
from components.test_generator_tab import render_test_generator_tab

# Load environment variables from .env file (API key, defaults)
load_dotenv()

st.set_page_config(
    page_title="Code Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Code Assistant App")
st.markdown("""
This app helps you analyze, optimize, review, and compare code using AI agents.
Upload your code files and let the AI do the work!
""")

# Initialize session state defaults
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-4o-mini"
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.2

# Render sidebar and get API key
api_key = render_sidebar()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Code Optimization",
    "Code Review",
    "Code Comparison",
    "Test Generator",
])

with tab1:
    render_optimizer_tab(api_key)

with tab2:
    render_reviewer_tab(api_key)

with tab3:
    render_comparer_tab(api_key)

with tab4:
    render_test_generator_tab(api_key)

st.markdown("---")
st.markdown("Code Assistant App. Copyright 2025 By Gaurav Mane. All rights reserved.")
