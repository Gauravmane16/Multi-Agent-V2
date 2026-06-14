"""
Sidebar component for the Code Assistant App.
"""

import streamlit as st
from typing import Optional


def render_sidebar() -> Optional[str]:
    """
    Render the sidebar with configuration options.

    Returns:
        Optional[str]: The API key if set, None otherwise.
    """
    with st.sidebar:
        st.subheader("Configuration")

        with st.expander("ℹ️ How to get OpenAI API Key", expanded=False):
            st.markdown("""
            To get your OpenAI API key:
            1. Go to [OpenAI API Platform](https://platform.openai.com/signup)
            2. Create an account or sign in
            3. Navigate to [API Keys section](https://platform.openai.com/api-keys)
            4. Click 'Create new secret key'
            5. Copy the key (it won't be shown again)

            **Note**: OpenAI API is a paid service; new accounts receive free credits.

            [View OpenAI's Pricing](https://openai.com/pricing)
            """)

        api_key = st.text_input("Enter your OpenAI API key", type="password")

        if api_key:
            st.success("API key set successfully!")
        else:
            st.warning("Please enter your OpenAI API key to use the app.")

        with st.expander("Advanced Settings"):
            model = st.selectbox(
                "Model",
                options=[
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-4",
                    "gpt-3.5-turbo",
                ],
                index=1,  # default: gpt-4o-mini (fast + cheap)
                help="gpt-4o-mini is recommended for most tasks — fast and cost-effective."
            )

            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.2,
                step=0.1,
                help="Higher values make output more creative; lower values more deterministic."
            )

            st.session_state["model"] = model
            st.session_state["temperature"] = temperature

        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This app provides four main functionalities:
        1. **Code Optimization** — Improves efficiency and readability
        2. **Code Review** — Finds bugs, security issues, and best-practice violations
        3. **Code Comparison** — Analyses differences between two files
        4. **Test Generator** — Creates unit tests for your code
        """)

        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit and LangChain by Gaurav Mane")

    return api_key
