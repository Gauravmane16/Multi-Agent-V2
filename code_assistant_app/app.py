"""
Main application file for the Code Assistant App.
"""

import streamlit as st
import os
# from dotenv import load_dotenv
from components.sidebar import render_sidebar
from components.optimizer_tab import render_optimizer_tab
from components.reviewer_tab import render_reviewer_tab
from components.comparer_tab import render_comparer_tab

# Load environment variables from .env file
# load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Code Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("Code Assistant App")
st.markdown("""
This app helps you analyze, optimize, review, and compare code using AI agents.
Upload your code files and let the AI do the work!
""")

# Initialize session state for model settings if not already done
if "model" not in st.session_state:
    st.session_state["model"] = "gpt-3.5-turbo-16k"
if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.2

# Render sidebar and get API key
api_key = render_sidebar()

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Code Optimization", "Code Review", "Code Comparison"])

# Render each tab
with tab1:
    render_optimizer_tab(api_key)

with tab2:
    render_reviewer_tab(api_key)

with tab3:
    render_comparer_tab(api_key)

# Add a footer
st.markdown("---")
st.markdown("Code Assistant App. Copyright-2025 By Gaurav Mane. All rights reserved.")