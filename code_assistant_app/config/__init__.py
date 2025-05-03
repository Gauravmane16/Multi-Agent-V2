"""
Config module for the Code Assistant App.
"""

import os
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# # API Key settings
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo-16k")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# Chunking settings
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200