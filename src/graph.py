from langgraph.graph import StateGraph, END

from src.state import AgentState

from .router import router_node
from .researcher import researcher_node
from .product import pm_agent_node
from .technical import tech_agent_node
from .summarizer import summarizer_node

workflow = StateGraph(AgentState)

workflow.add_node("router",router_node)
workflow.add_node("researcher",researcher_node)
workflow.add_node("pm",pm_agent_node)
workflow.add_node("tech",tech_agent_node)
workflow.add_node("summarizer",summarizer_node)
workflow.set_entry_point("router")

def route_after_router(state):
    return "researcher"

workflow.add_conditional_edges("router",route_after_router,{"researcher": "researcher"})

def route_after_researcher(state):
    if state["intent"] == "documentation":
        return "pm"

    return "tech"

workflow.add_conditional_edges("researcher",route_after_researcher,{"pm": "pm","tech": "tech"})
workflow.add_edge("pm","summarizer")
workflow.add_edge("tech","summarizer")
workflow.add_edge("summarizer",END)

graph = workflow.compile()