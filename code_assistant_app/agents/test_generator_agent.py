"""
Unit test generator agent for the Code Assistant App.
"""

from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from typing import Optional, Dict, List, Union
import zipfile
import io


def create_test_generator_agent(api_key: str, model_name: str, temperature: float) -> Optional[object]:
    """
    Create an AI agent for generating unit tests.
    
    Args:
        api_key: OpenAI API key
        model_name: Name of the model (from UI selection)
        temperature: Temperature value (from UI selection)
        
    Returns:
        object: LangChain agent for test generation or None if error
    """
    try:
        # Create LLM
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key
        )
        
        # Create chat prompt
        system_template = """You are a test generation specialist. Your task is to:
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

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        # Create test generation chain
        test_chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        # Create tools
        tools = [
            Tool(
                name="GenerateTests",
                func=lambda x: test_chain.run(input=x),
                description="Generate unit tests for the provided code"
            )
        ]
        
        # Initialize agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        return agent
    
    except Exception as e:
        print(f"Error creating test generator agent: {str(e)}")
        return None


def generate_tests_for_file(agent: object, code_content: str, 
                           filename: str) -> Dict[str, str]:
    """
    Generate unit tests for a single file.
    
    Args:
        agent: LangChain agent for test generation
        code_content: Code to generate tests for
        filename: Name of the file
        
    Returns:
        Dict[str, str]: Dictionary containing test results
    """
    try:
        # Prepare input with file information
        input_text = f"""Generate unit tests for the following code from {filename}:

{code_content}

Please provide complete test file content including imports and proper test structure."""

        # Generate tests
        test_result = agent.run(input=input_text)
        
        return {
            "filename": f"test_{filename}",
            "content": test_result
        }
    except Exception as e:
        return {
            "filename": f"test_{filename}",
            "content": f"Error generating tests: {str(e)}"
        }


def generate_tests_for_multiple_files(agent: object, 
                                    files: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Generate unit tests for multiple files.
    
    Args:
        agent: LangChain agent for test generation
        files: List of dictionaries containing filename and content
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing test results
    """
    results = []
    for file_info in files:
        result = generate_tests_for_file(
            agent,
            file_info["content"],
            file_info["filename"]
        )
        results.append(result)
    return results


def process_zip_file(zip_content: bytes) -> List[Dict[str, str]]:
    """
    Process a zip file and extract code files.
    
    Args:
        zip_content: Bytes content of the zip file
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing filename and content
    """
    files = []
    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
        for filename in z.namelist():
            if filename.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.cs')):
                with z.open(filename) as f:
                    content = f.read().decode('utf-8')
                    files.append({
                        "filename": filename,
                        "content": content
                    })
    return files