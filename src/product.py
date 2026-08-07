from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .state import AgentState
from .models import gpt_groq
from .utils import open_md

PM_PROMPT =  open_md("product.md")

prompt = ChatPromptTemplate.from_messages([("system", PM_PROMPT),("human","""contexto da documentação:{context}""")])

llm = gpt_groq()

pm_chain = (prompt | llm | JsonOutputParser())

def pm_agent_node(state: AgentState):

    documents = state["researcher_output"]["documents"]

    context = "\n\n".join([document["content"] for document in documents])

    result = pm_chain.invoke({"context": context})

    return {"product_output": result}