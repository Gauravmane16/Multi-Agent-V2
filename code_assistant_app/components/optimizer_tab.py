"""
Optimizer tab component for the Code Assistant App.
"""

import streamlit as st
from utils.file_utils import read_uploaded_file, detect_language
from utils.visualization import display_code_with_line_numbers, display_markdown_result
from agents.optimizer_agent import create_optimizer_agent, optimize_code


def render_optimizer_tab(api_key: str) -> None:
    """
    Render the code optimization tab.
    
    Args:
        api_key: OpenAI API key
    """
    st.header("Code Optimization")
    st.write("Upload your code file to receive optimization suggestions.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your code file", key="optimizer_file")

    if uploaded_file:
        # Get file content and language
        code_content = read_uploaded_file(uploaded_file)
        language = detect_language(uploaded_file.name)
        
        # Display the code
        st.subheader("Original Code")
        display_code_with_line_numbers(code_content, language)
        
        # Optimize button
        if st.button("Optimize Code", key="optimize_btn"):
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar first.")
            else:
                try:
                    with st.spinner("Analyzing and optimizing your code..."):
                        # Get model settings from session state
                        model = st.session_state.get("model", "gpt-3.5-turbo-16k")
                        temperature = st.session_state.get("temperature", 0.2)
                        
                        # Create optimizer agent
                        optimizer_agent = create_optimizer_agent(
                            api_key=api_key,
                            model_name=model,
                            temperature=temperature
                        )
                        
                        if optimizer_agent:
                            # Run optimization
                            optimization_result = optimize_code(optimizer_agent, code_content)
                            
                            # Display results
                            st.subheader("Optimization Results")
                            display_markdown_result(optimization_result)
                        else:
                            st.error("Failed to create optimizer agent.")
                            
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a code file to get started.")