from langchain_core.prompts import ChatPromptTemplate

from state import AgentState
from src.models import llama_groq
from src.utils import open_md

SUMMARIZER_PROMPT = open_md("summarizer.md")
llm = llama_groq()
prompt = ChatPromptTemplate.from_messages([("system",SUMMARIZER_PROMPT),("human","""Dados da análise:{analysis}""")])
summarizer_chain = (prompt| llm)

def summarizer_node(state: AgentState):

    if state["intent"] == "documentation":
        analysis = state["product_output"]

    else:
        analysis = state["technical_output"]

    response = summarizer_chain.invoke({"analysis": analysis})
    return {"final_answer": response.content}