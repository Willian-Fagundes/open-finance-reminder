import os

from src.state import AgentState
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv(override=True)

HF_TOKEN = os.environ.get("HF_TOKEN")
BD_PATH = "./data/DB"

embedding = HuggingFaceEmbeddings(
    model_name="google/embeddinggemma-300m",
    model_kwargs={
        "token": HF_TOKEN
    }
)

db = Chroma(
    persist_directory=BD_PATH,
    embedding_function=embedding
)

def researcher_node(state: AgentState):

    question = state["question"]
    results = db.similarity_search_with_relevance_scores(
        query=question,
        k=3
    )

    documents = []


    for document, score in results:

        documents.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "score": float(score)
            }
        )


    return {
        "retrieved_chunks": documents,

        "researcher_output": {
            "status": "success" if documents else "not_found",
            "documents": documents,
            "total_documents": len(documents)
        }
    }