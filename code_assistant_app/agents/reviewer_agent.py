"""
Code review agent for the Code Assistant App.
Uses modern LangChain LCEL (pipe) pattern — no deprecated LLMChain or initialize_agent.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from config.prompts import REVIEWER_SYSTEM_TEMPLATE
from typing import Optional


def create_reviewer_agent(api_key: str, model_name: str = "gpt-4o-mini",
                          temperature: float = 0.2) -> Optional[object]:
    """
    Create an LCEL chain for code review.

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
            SystemMessagePromptTemplate.from_template(REVIEWER_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template("{code_content}")
        ])

        chain = chat_prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        print(f"Error creating reviewer agent: {str(e)}")
        return None


def review_code(chain: object, code_content: str) -> str:
    """
    Review the provided code using the LCEL chain.
    """
    try:
        return chain.invoke({"code_content": code_content})
    except Exception as e:
        return f"Error during code review: {str(e)}"
