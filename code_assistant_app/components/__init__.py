"""
Components package for the Code Assistant App.
"""

from components.sidebar import render_sidebar
from components.optimizer_tab import render_optimizer_tab
from components.reviewer_tab import render_reviewer_tab
from components.comparer_tab import render_comparer_tab
from components.test_generator_tab import render_test_generator_tab  # Add this import

__all__ = [
    'render_sidebar',
    'render_optimizer_tab',
    'render_reviewer_tab',
    'render_comparer_tab',
    'render_test_generator_tab'  # Add this export
]