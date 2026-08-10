from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from state import AgentState
from src.models import gpt_groq
from src.utils import open_md

TECH_PROMPT =  open_md("technical.md")

llm = gpt_groq()
prompt = ChatPromptTemplate.from_messages([("system",TECH_PROMPT),("human","""Pergunta do usuário: {question}Código: {code}Documentação encontrada: {context}""")])
tech_chain = (prompt | llm | JsonOutputParser())

def tech_agent_node(state: AgentState):

    documents = state["researcher_output"]["documents"]
    context = "\n\n".join([doc["content"]for doc in documents])
    result = tech_chain.invoke({"question": state["question"],"code": state.get("code","Nenhum código fornecido"),"context": context})
    return {"technical_output": result}
