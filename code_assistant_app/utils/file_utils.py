"""
Utilities for file handling in the Code Assistant App.
"""

import streamlit as st
from tempfile import NamedTemporaryFile
import os
from typing import List, Optional, Dict, Any, Tuple


def read_uploaded_file(uploaded_file) -> str:
    """
    Read the content of an uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Content of the file as string
    """
    if uploaded_file is not None:
        content = uploaded_file.getvalue().decode("utf-8")
        return content
    return ""


def detect_language(filename: str) -> str:
    """
    Detect the programming language based on file extension.
    
    Args:
        filename: Name of the file
    
    Returns:
        str: Detected language name or 'text' if not recognized
    """
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.rs': 'rust',
        '.sh': 'bash',
        '.sql': 'sql',
        '.r': 'r',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown'
    }
    
    _, ext = os.path.splitext(filename)
    return extension_map.get(ext.lower(), 'text')


def save_uploaded_file(uploaded_file) -> Tuple[str, str]:
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple[str, str]: (File path, detected language)
    """
    if uploaded_file is None:
        return "", "text"
    
    content = uploaded_file.getvalue()
    language = detect_language(uploaded_file.name)
    
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(content)
        return tmp.name, language