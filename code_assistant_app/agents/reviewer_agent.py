"""
Code review agent for the Code Assistant App.
"""

from langchain_openai import ChatOpenAI 
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.prompts import REVIEWER_SYSTEM_TEMPLATE, HUMAN_TEMPLATE
from typing import Optional


def create_reviewer_agent(api_key: str, model_name: str = "gpt-3.5-turbo-16k", 
                         temperature: float = 0.2) -> Optional[object]:
    """
    Create an AI agent for code review.
    
    Args:
        api_key: OpenAI API key
        model_name: Name of the model to use
        temperature: Temperature for the model
        
    Returns:
        object: LangChain agent for code review or None if error
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
        
        # Create system and human message templates
        system_message_prompt = SystemMessagePromptTemplate.from_template(REVIEWER_SYSTEM_TEMPLATE)
        human_message_prompt = HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
        
        # Create chat prompt
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])
        
        # Create analysis chain
        analyze_chain = LLMChain(llm=llm, prompt=chat_prompt)
        
        # Create tools
        tools = [
            Tool(
                name="ReviewCode",
                func=lambda code: analyze_chain.run(code_content=code),
                description="Analyze code and provide review feedback"
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
        print(f"Error creating reviewer agent: {str(e)}")
        return None


def review_code(agent: object, code_content: str) -> str:
    """
    Review the provided code using the agent.
    
    Args:
        agent: LangChain agent for code review
        code_content: Code to review
        
    Returns:
        str: Review result
    """
    try:
        review_result = agent.run(code_content)
        return review_result
    except Exception as e:
        return f"Error during code review: {str(e)}"