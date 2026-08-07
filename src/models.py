# gemini -> orquestrador
# deepseek -> coding
# llama -> summarizer
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv(override = True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def gpt_groq():
    llm_groq_gpt = ChatGroq(model = "openai/gpt-oss-120b",
                        temperature= 0.1, max_tokens=None,
                        timeout=None,
                        api_key=GROQ_API_KEY)
    return llm_groq_gpt

def llama_groq():
    llm_groq_llama = ChatGroq(model = "llama-3.1-8b-instant",
                             temperature=0.1, max_tokens = None,
                             timeout=None,
                             api_key=GROQ_API_KEY)
    return llm_groq_llama