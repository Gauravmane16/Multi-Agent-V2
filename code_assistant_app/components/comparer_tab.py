"""
Comparer tab component for the Code Assistant App.
"""

import streamlit as st
from utils.file_utils import read_uploaded_file, detect_language
from utils.visualization import display_code_with_line_numbers, display_markdown_result, display_diff
from agents.comparer_agent import create_comparer_agent, compare_code


def render_comparer_tab(api_key: str) -> None:
    """
    Render the code comparison tab.
    
    Args:
        api_key: OpenAI API key
    """
    st.header("Code Comparison")
    st.write("Upload two code files to compare them.")
    
    # Create two columns for file upload
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("First Code File")
        first_file = st.file_uploader("Upload first code file", key="first_file")
        first_code = ""
        first_language = "text"
        
        if first_file:
            first_code = read_uploaded_file(first_file)
            first_language = detect_language(first_file.name)
            display_code_with_line_numbers(first_code, first_language)
    
    with col2:
        st.subheader("Second Code File")
        second_file = st.file_uploader("Upload second code file", key="second_file")
        second_code = ""
        second_language = "text"
        
        if second_file:
            second_code = read_uploaded_file(second_file)
            second_language = detect_language(second_file.name)
            display_code_with_line_numbers(second_code, second_language)
    
    # Compare button (only if both files are uploaded)
    if first_file and second_file:
        if st.button("Compare Code", key="compare_btn"):
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar first.")
            else:
                try:
                    with st.spinner("Comparing code files..."):
                        # Get model settings from session state
                        model = st.session_state.get("model", "gpt-3.5-turbo-16k")
                        temperature = st.session_state.get("temperature", 0.2)
                        
                        # Create comparer agent
                        comparer_agent = create_comparer_agent(
                            api_key=api_key,
                            model_name=model,
                            temperature=temperature
                        )
                        
                        if comparer_agent:
                            # Run comparison
                            comparison_result = compare_code(comparer_agent, first_code, second_code)
                            
                            # Display AI analysis
                            st.subheader("AI Analysis")
                            display_markdown_result(comparison_result)
                            
                            # Display visual diff
                            st.subheader("Visual Diff")
                            display_diff(
                                first_code, 
                                second_code, 
                                first_label=first_file.name if first_file else "First File", 
                                second_label=second_file.name if second_file else "Second File"
                            )
                        else:
                            st.error("Failed to create comparer agent.")
                            
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    elif first_file or second_file:
        st.warning("Please upload both files to compare them.")
    else:
        st.info("Please upload two code files to get started.")