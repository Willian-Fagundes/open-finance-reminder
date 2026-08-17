from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from state import AgentState
from src.models import gpt_groq, llama_groq
from src.utils import open_md

ROUTER_PROMPT = open_md("router.md")
QUESTION_IMPROVER_PROMPT = open_md("question_improver.md")

llm = llama_groq()

# Chain para classificar intenção
intent_prompt = ChatPromptTemplate.from_messages([("system", ROUTER_PROMPT), ("human", "{question}")])
intent_chain = (intent_prompt | llm | JsonOutputParser())

# Chain para melhorar pergunta
improver_prompt = ChatPromptTemplate.from_template(QUESTION_IMPROVER_PROMPT)
improver_chain = (improver_prompt | llm | JsonOutputParser())


def improve_question(question: str) -> dict:
    """Melhora a pergunta para otimizar a busca no researcher"""
    result = improver_chain.invoke({"question": question})
    return result


def router_node(state: AgentState):
    """
    Node do router que:
    1. Classifica a intenção da pergunta
    2. Melhora/refina a pergunta para melhor recuperação
    """
    question = state["question"]
    
    # Classificar intenção
    intent_result = intent_chain.invoke({"question": question})
    
    # Melhorar pergunta para o researcher
    improved_result = improve_question(question)
    
    return {
        "intent": intent_result["intent"],
        "confidence": intent_result["confidence"],
        "retrieval_query": improved_result["pergunta_melhorada"]
    }
