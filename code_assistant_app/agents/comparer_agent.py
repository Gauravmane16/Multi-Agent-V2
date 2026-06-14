"""
Code comparison agent for the Code Assistant App.
Uses modern LangChain LCEL (pipe) pattern — no deprecated LLMChain or initialize_agent.
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.prompts import COMPARE_TEMPLATE
from typing import Optional


def create_comparer_agent(api_key: str, model_name: str = "gpt-4o-mini",
                          temperature: float = 0.2) -> Optional[object]:
    """
    Create an LCEL chain for code comparison.

    Returns:
        Runnable chain or None on error.
    """
    try:
        llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )

        compare_prompt = PromptTemplate(
            template=COMPARE_TEMPLATE,
            input_variables=["first_code", "second_code"]
        )

        chain = compare_prompt | llm | StrOutputParser()
        return chain

    except Exception as e:
        print(f"Error creating comparer agent: {str(e)}")
        return None


def compare_code(chain: object, first_code: str, second_code: str) -> str:
    """
    Compare two code files using the LCEL chain.
    """
    try:
        return chain.invoke({"first_code": first_code, "second_code": second_code})
    except Exception as e:
        return f"Error during code comparison: {str(e)}"
