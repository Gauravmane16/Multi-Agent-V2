"""
Visualization utilities for the Code Assistant App.
"""

import streamlit as st
import difflib
from typing import List


def display_code_with_line_numbers(code: str, language: str = "python") -> None:
    """
    Display code with line numbers in Streamlit.
    
    Args:
        code: The code to display
        language: The programming language for syntax highlighting
    """
    st.code(code, language=language, line_numbers=True)


def generate_html_diff(first_code: str, second_code: str, first_label: str = "First File", 
                      second_label: str = "Second File") -> str:
    """
    Generate an HTML diff view of two code snippets.
    
    Args:
        first_code: First code snippet
        second_code: Second code snippet
        first_label: Label for the first code snippet
        second_label: Label for the second code snippet
        
    Returns:
        str: HTML representation of the diff
    """
    diff = difflib.HtmlDiff().make_file(
        first_code.splitlines(),
        second_code.splitlines(),
        first_label,
        second_label
    )
    return diff


def display_diff(first_code: str, second_code: str, first_label: str = "First File", 
                second_label: str = "Second File", height: int = 500) -> None:
    """
    Display a visual diff of two code snippets in Streamlit.
    
    Args:
        first_code: First code snippet
        second_code: Second code snippet
        first_label: Label for the first code snippet
        second_label: Label for the second code snippet
        height: Height of the diff component
    """
    diff = generate_html_diff(first_code, second_code, first_label, second_label)
    st.components.v1.html(diff, height=height, scrolling=True)


def display_markdown_result(result: str) -> None:
    """
    Display a markdown result with proper formatting.
    
    Args:
        result: Markdown text to display
    """
    st.markdown(result)