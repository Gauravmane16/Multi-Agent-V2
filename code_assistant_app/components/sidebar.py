"""
Sidebar component for the Code Assistant App.
"""

import streamlit as st
from typing import Optional


def render_sidebar() -> Optional[str]:
    """
    Render the sidebar with configuration options.
    
    Returns:
        Optional[str]: The API key if set, None otherwise
    """
    with st.sidebar:
        st.subheader("Configuration")
        
        # API Key input with help information
        with st.expander("ℹ️ How to get OpenAI API Key", expanded=False):
            st.markdown("""
            To get your OpenAI API key:
            1. Go to [OpenAI API Platform](https://platform.openai.com/signup)
            2. Create an account or sign in
            3. Navigate to [API Keys section](https://platform.openai.com/api-keys)
            4. Click 'Create new secret key'
            5. Copy the key (make sure to save it as it won't be shown again)
            
            **Note**: OpenAI API is a paid service. You'll need to add billing 
            information to use the API. New accounts get some free credits to start.
            
            [View OpenAI's Pricing](https://openai.com/pricing)
            """)
        
        # API Key input
        api_key = st.text_input("Enter your OpenAI API key", type="password")
        
        if api_key:
            st.success("API key set successfully!")
        else:
            st.warning("Please enter your OpenAI API key to use the app.")
        
        # Advanced settings expander
        with st.expander("Advanced Settings"):
            model = st.selectbox(
                "Model",
                options=["gpt-3.5-turbo-16k", "gpt-4", "gpt-4-turbo"],
                index=0
            )
            
            temperature = st.slider(
                "Temperature", 
                min_value=0.0, 
                max_value=1.0, 
                value=0.2, 
                step=0.1,
                help="Higher values make output more random, lower values more deterministic"
            )
            
            st.session_state["model"] = model
            st.session_state["temperature"] = temperature
        
        # About section
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app provides three main functionalities:
        1. **Code Optimization** - Improves your code's efficiency and readability
        2. **Code Review** - Reviews your code for bugs, security issues, and best practices
        3. **Code Comparison** - Compares two code files and analyzes differences
        """)
        
        # Footer
        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit and LangChain by Gaurav Mane")
    
    return api_key