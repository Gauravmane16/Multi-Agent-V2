"""
Code optimization agent for the Code Assistant App.
Uses modern LangChain LCEL (pipe) pattern — no deprecated LLMChain or initialize_agent.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from config.prompts import OPTIMIZER_SYSTEM_TEMPLATE
from typing import Optional


def create_optimizer_agent(api_key: str, model_name: str = "gpt-4o-mini",
                           temperature: float = 0.2) -> Optional[object]:
    """
    Create an LCEL chain for code optimization.

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
            SystemMessagePromptTemplate.from_template(OPTIMIZER_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        chain = chat_prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        print(f"Error creating optimizer agent: {str(e)}")
        return None


def optimize_code(chain: object, code_content: str) -> str:
    """
    Optimize the provided code using the LCEL chain.
    """
    try:
        return chain.invoke({"input": code_content})
    except Exception as e:
        return f"Error during optimization: {str(e)}"
