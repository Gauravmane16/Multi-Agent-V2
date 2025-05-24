"""
Test generator tab component for the Code Assistant App.
"""

import streamlit as st
from utils.file_utils import read_uploaded_file, detect_language
from utils.visualization import display_code_with_line_numbers
from agents.test_generator_agent import (
    create_test_generator_agent,
    generate_tests_for_multiple_files,
    process_zip_file
)
from typing import List, Dict


def render_test_generator_tab(api_key: str) -> None:
    """
    Render the test generator tab.
    
    Args:
        api_key: OpenAI API key
    """
    st.header("Unit Test Generator")
    st.write("Upload your code file(s) to generate unit tests.")
    
    # Upload type selection
    upload_type = st.radio(
        "Choose upload type:",
        ["Single File", "Multiple Files", "Zip File"]
    )
    
    if upload_type == "Single File":
        # Single file upload
        uploaded_file = st.file_uploader(
            "Upload your code file",
            key="test_gen_single"
        )
        
        if uploaded_file:
            code_content = read_uploaded_file(uploaded_file)
            language = detect_language(uploaded_file.name)
            
            st.subheader("Source Code")
            display_code_with_line_numbers(code_content, language)
            
            if st.button("Generate Tests", key="gen_test_single"):
                handle_test_generation(api_key, [{"filename": uploaded_file.name, "content": code_content}])
                
    elif upload_type == "Multiple Files":
        # Multiple files upload
        uploaded_files = st.file_uploader(
            "Upload your code files",
            accept_multiple_files=True,
            key="test_gen_multiple"
        )
        
        if uploaded_files:
            files_data = []
            for uploaded_file in uploaded_files:
                code_content = read_uploaded_file(uploaded_file)
                language = detect_language(uploaded_file.name)
                
                st.subheader(f"Source Code: {uploaded_file.name}")
                display_code_with_line_numbers(code_content, language)
                
                files_data.append({
                    "filename": uploaded_file.name,
                    "content": code_content
                })
            
            if st.button("Generate Tests", key="gen_test_multiple"):
                handle_test_generation(api_key, files_data)
                
    else:  # Zip File
        # Zip file upload
        uploaded_zip = st.file_uploader(
            "Upload your zip file containing code files",
            type="zip",
            key="test_gen_zip"
        )
        
        if uploaded_zip:
            try:
                files_data = process_zip_file(uploaded_zip.getvalue())
                
                if files_data:
                    st.subheader("Found Files:")
                    for file_info in files_data:
                        st.write(f"- {file_info['filename']}")
                        with st.expander(f"View {file_info['filename']}"):
                            language = detect_language(file_info['filename'])
                            display_code_with_line_numbers(file_info['content'], language)
                    
                    if st.button("Generate Tests", key="gen_test_zip"):
                        handle_test_generation(api_key, files_data)
                else:
                    st.warning("No supported code files found in the zip archive.")
                    
            except Exception as e:
                st.error(f"Error processing zip file: {str(e)}")


def handle_test_generation(api_key: str, files_data: List[Dict[str, str]]) -> None:
    """
    Handle test generation for the uploaded files.
    
    Args:
        api_key: OpenAI API key
        files_data: List of dictionaries containing filename and content
    """
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar first.")
        return
        
    try:
        with st.spinner("Generating unit tests..."):
            # Get model settings from session state
            model = st.session_state.get("selected_model", "gpt-4")  # Default to GPT-4 if not set
            temperature = st.session_state.get("temperature", 0.7)    # Default to 0.7 if not set
            
            # Create test generator agent with UI-selected parameters
            agent = create_test_generator_agent(
                api_key=api_key,
                model_name=model,
                temperature=temperature
            )
            
            if agent:
                # Generate tests
                test_results = generate_tests_for_multiple_files(agent, files_data)
                
                # Display results
                st.subheader("Generated Unit Tests")
                for result in test_results:
                    with st.expander(f"Tests for {result['filename']}"):
                        display_code_with_line_numbers(
                            result['content'],
                            detect_language(result['filename'])
                        )
                        
                        # Add download button for each test file
                        st.download_button(
                            f"Download {result['filename']}",
                            result['content'],
                            file_name=result['filename'],
                            mime="text/plain"
                        )
            else:
                st.error("Failed to create test generator agent.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")