"""
Unit test generator agent for the Code Assistant App.
Uses modern LangChain LCEL (pipe) pattern — no deprecated LLMChain or initialize_agent.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, Dict, List
import zipfile
import io


_SYSTEM_TEMPLATE = """You are a test generation specialist. Your task is to:
1. Analyze the provided code and understand its functionality
2. Generate comprehensive unit tests that cover:
   - Main functionality
   - Edge cases
   - Error scenarios
   - Input validation
3. Use appropriate testing frameworks (e.g., pytest for Python)
4. Include setup and teardown if needed
5. Add clear comments explaining test cases

Remember to:
- Follow testing best practices
- Include assertion messages
- Use meaningful test names
- Group related tests
- Mock external dependencies when needed"""


def create_test_generator_agent(api_key: str, model_name: str = "gpt-4o-mini",
                                temperature: float = 0.2) -> Optional[object]:
    """
    Create an LCEL chain for unit test generation.

    Returns:
        Runnable chain or None on error.
    """
    try:
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        chain = chat_prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        print(f"Error creating test generator agent: {str(e)}")
        return None


def generate_tests_for_file(chain: object, code_content: str,
                            filename: str) -> Dict[str, str]:
    """
    Generate unit tests for a single file.
    """
    try:
        input_text = (
            f"Generate unit tests for the following code from {filename}:\n\n"
            f"{code_content}\n\n"
            "Please provide complete test file content including imports and proper test structure."
        )
        result = chain.invoke({"input": input_text})
        return {"filename": f"test_{filename}", "content": result}
    except Exception as e:
        return {"filename": f"test_{filename}", "content": f"Error generating tests: {str(e)}"}


def generate_tests_for_multiple_files(chain: object,
                                      files: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Generate unit tests for multiple files.
    """
    return [generate_tests_for_file(chain, f["content"], f["filename"]) for f in files]


def process_zip_file(zip_content: bytes) -> List[Dict[str, str]]:
    """
    Process a zip file and extract supported code files.
    """
    files = []
    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
        for filename in z.namelist():
            if filename.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.cs')):
                with z.open(filename) as f:
                    content = f.read().decode('utf-8')
                    files.append({"filename": filename, "content": content})
    return files
