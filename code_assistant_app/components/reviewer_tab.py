"""
Reviewer tab component for the Code Assistant App.
"""

import streamlit as st
from utils.file_utils import read_uploaded_file, detect_language
from utils.visualization import display_code_with_line_numbers, display_markdown_result
from agents.reviewer_agent import create_reviewer_agent, review_code


def render_reviewer_tab(api_key: str) -> None:
    """
    Render the code review tab.
    
    Args:
        api_key: OpenAI API key
    """
    st.header("Code Review")
    st.write("Upload your code file to receive a detailed code review.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your code file", key="reviewer_file")

    if uploaded_file:
        # Get file content and language
        code_content = read_uploaded_file(uploaded_file)
        language = detect_language(uploaded_file.name)
        
        # Display the code
        st.subheader("Code to Review")
        display_code_with_line_numbers(code_content, language)
        
        # Review button
        if st.button("Review Code", key="review_btn"):
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar first.")
            else:
                try:
                    with st.spinner("Analyzing and reviewing your code..."):
                        # Get model settings from session state
                        model = st.session_state.get("model", "gpt-3.5-turbo-16k")
                        temperature = st.session_state.get("temperature", 0.2)
                        
                        # Create reviewer agent
                        reviewer_agent = create_reviewer_agent(
                            api_key=api_key,
                            model_name=model,
                            temperature=temperature
                        )
                        
                        if reviewer_agent:
                            # Run review
                            review_result = review_code(reviewer_agent, code_content)
                            
                            # Display results
                            st.subheader("Review Results")
                            display_markdown_result(review_result)
                        else:
                            st.error("Failed to create reviewer agent.")
                            
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please upload a code file to get started.")