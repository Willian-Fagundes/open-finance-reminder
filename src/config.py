import os
from dotenv import load_dotenv

load_dotenv(override=True)

HF_TOKEN = os.environ.get("HF_TOKEN")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")