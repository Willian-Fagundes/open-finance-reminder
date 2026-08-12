import os
import chromadb
from src.utils import search_web
from state import AgentState
from dotenv import load_dotenv
from langchain_chroma import Chroma
from huggingface_hub import InferenceClient
from langchain_core.embeddings import Embeddings


load_dotenv(override=True)

HF_TOKEN = os.environ.get("HF_TOKEN")
CHROMA_API_KEY = os.environ.get("CHROMA_API_KEY")
CHROMA_TENANT = os.environ.get("CHROMA_TENANT")
CHROMA_DATABASE = os.environ.get("CHROMA_DATABASE")
CHROMA_COLLECTION  = os.environ.get("CHROMA_COLLECTION")

class HFRemoteEmbeddings(Embeddings):
    def __init__(self, model_name: str, token: str):
        self.client = InferenceClient(model=model_name, token=token)

    def embed_query(self, text: str) -> list[float]:
        result = self.client.feature_extraction(text)
        return result[0] if hasattr(result, "__len__") and len(result) and hasattr(result[0], "__len__") else result

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(t) for t in texts]

chroma_client = chromadb.CloudClient(api_key = CHROMA_API_KEY,
                                     tenant = CHROMA_TENANT,
                                     database = CHROMA_DATABASE)



embedding = HFRemoteEmbeddings(
    model_name="google/embeddinggemma-300m",
    token=HF_TOKEN
)

db = Chroma(
    client = chroma_client,
    collection_name= CHROMA_COLLECTION,
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


def web_search_node(state: AgentState):
    query = state["question"]
    results = search_web(query, max_results=4)

    documents = []
    for result in results:
        content = result.get("body") or result.get("text") or result.get("snippet") or ""
        documents.append(
            {
                "content": content,
                "metadata": {
                    "source": result.get("href") or result.get("url") or result.get("source", ""),
                    "title": result.get("title", "")
                },
                "score": 0.0
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
