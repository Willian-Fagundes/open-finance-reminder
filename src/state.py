from typing import TypedDict, List, Literal

class Findings(TypedDict):
    title : str
    content : str
    source : str
    similarity : float

class ResearcherOutput(TypedDict):
    status : str
    findings : List[Findings]

class APIreference(TypedDict):
    name : str
    description : str

class ProductOutput(TypedDict):
    topic : str
    explanation : str
    api_references : List[APIreference]
    flows : List[str]
    notes : List[str]

class TechnicalOutput(TypedDict):
    diagnosis: str
    severity: Literal["low", "medium", "high"]
    recommendations: List[str]
    references: List[str]

class AgentState(TypedDict, total=False):
    # Input
    question: str
    code: str
    conversation_history: List[dict]
    retrieval_context: str
    # Router
    intent: Literal["documentation", "technical_support"]
    confidence: float
    # Retrieval
    retrieval_query: str
    researcher_output: ResearcherOutput
    # Specialist
    product_output: ProductOutput
    technical_output: TechnicalOutput
    # Final
    final_answer: str