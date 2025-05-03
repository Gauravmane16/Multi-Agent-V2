"""
Utilities package for the Code Assistant App.
"""

from utils.file_utils import read_uploaded_file, detect_language, save_uploaded_file
from utils.visualization import display_code_with_line_numbers, generate_html_diff, display_diff, display_markdown_result

__all__ = [
    'read_uploaded_file',
    'detect_language',
    'save_uploaded_file',
    'display_code_with_line_numbers',
    'generate_html_diff',
    'display_diff',
    'display_markdown_result'
]