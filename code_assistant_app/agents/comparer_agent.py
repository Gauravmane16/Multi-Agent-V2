"""
Code comparison agent for the Code Assistant App.
"""

from langchain_openai import ChatOpenAI 
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.prompts import COMPARER_SYSTEM_TEMPLATE, COMPARE_TEMPLATE
from typing import Optional, Dict, Any


def create_comparer_agent(api_key: str, model_name: str = "gpt-3.5-turbo-16k", 
                         temperature: float = 0.2) -> Optional[object]:
    """
    Create an AI agent for code comparison.
    
    Args:
        api_key: OpenAI API key
        model_name: Name of the model to use
        temperature: Temperature for the model
        
    Returns:
        object: LangChain agent for code comparison or None if error
    """
    try:
        # Create LLM
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key
        )
        
        # Create text splitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        
        # Create prompt for comparison
        compare_prompt = PromptTemplate(
            template=COMPARE_TEMPLATE,
            input_variables=["first_code", "second_code"]
        )
        
        # Create comparison chain
        compare_chain = LLMChain(llm=llm, prompt=compare_prompt)
        
        # Create tools
        tools = [
            Tool(
                name="CompareCodeFiles",
                func=lambda inputs: compare_chain.run(
                    first_code=inputs.get("first_code", ""),
                    second_code=inputs.get("second_code", "")
                ),
                description="Compare two code files and analyze their differences"
            )
        ]
        
        # Initialize agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        return agent
    
    except Exception as e:
        print(f"Error creating comparer agent: {str(e)}")
        return None


def compare_code(agent: object, first_code: str, second_code: str) -> str:
    """
    Compare the provided code files using the agent.
    
    Args:
        agent: LangChain agent for code comparison
        first_code: First code snippet
        second_code: Second code snippet
        
    Returns:
        str: Comparison result
    """
    try:
        input_data = {
            "first_code": first_code,
            "second_code": second_code
        }
        comparison_result = agent.run(input=input_data)
        return comparison_result
    except Exception as e:
        return f"Error during code comparison: {str(e)}"