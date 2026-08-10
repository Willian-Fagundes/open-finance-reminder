from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState
from src.models import gpt_groq, llama_groq
from src.utils import open_md

ROUTER_PROMPT = open_md("router.md")

llm = llama_groq()

prompt = ChatPromptTemplate.from_messages([("system",ROUTER_PROMPT),("human","{question}")])

router_chain = (prompt| llm| JsonOutputParser())

def router_node(state: AgentState):
    result = router_chain.invoke({"question": state["question"]})
    return {"intent": result["intent"],"confidence": result["confidence"]}
