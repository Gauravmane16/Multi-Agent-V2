"""
Code optimization agent for the Code Assistant App.
"""

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.prompts import OPTIMIZER_SYSTEM_TEMPLATE, HUMAN_TEMPLATE
from typing import Optional


def create_optimizer_agent(api_key: str, model_name: str = "gpt-3.5-turbo-16k", 
                         temperature: float = 0.2) -> Optional[object]:
    """
    Create an AI agent for code optimization.
    
    Args:
        api_key: OpenAI API key
        model_name: Name of the model to use
        temperature: Temperature for the model
        
    Returns:
        object: LangChain agent for code optimization or None if error
    """
    try:
        # Create LLM
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key
        )
        
        # Create chat prompt
        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(OPTIMIZER_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
        # Create analysis chain
        analyze_chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        # Create tools with proper input handling
        tools = [
            Tool(
                name="OptimizeCode",
                func=lambda x: analyze_chain.run(input=x),
                description="Analyze code and provide optimization suggestions"
            )
        ]
        
        # Initialize agent with handle_parsing_errors=True
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True  # Add this line
        )
        
        return agent
    
    except Exception as e:
        print(f"Error creating optimizer agent: {str(e)}")
        return None


def optimize_code(agent: object, code_content: str) -> str:
    """
    Optimize the provided code using the agent.
    
    Args:
        agent: LangChain agent for code optimization
        code_content: Code to optimize
        
    Returns:
        str: Optimization result
    """
    try:
        optimization_result = agent.run(input=code_content)  # Change this line
        return optimization_result
    except Exception as e:
        return f"Error during optimization: {str(e)}"