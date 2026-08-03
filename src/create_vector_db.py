
import time
import os

from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma.vectorstores import Chroma

load_dotenv(override= True)

HF_TOKEN = os.environ.get("HF_TOKEN")
BASE_DIR = Path("/workspaces/open-finance-reminder")
persist_directory = str(BASE_DIR / "agents" / "DB")
kb_path = Path("./kb_content.txt")

def load_txt(path):
    loader = TextLoader(str(path), encoding="utf-8")
    return loader.load()

def create_db(doc):
    print("starting db process")
    chunks = chunk_data(doc)
    vetorize_chunks(chunks)
    print("finishing db process")

def chunk_data(docs):
    print("starting chunck process")
    separate = RecursiveCharacterTextSplitter(
        chunk_size = 1024,
        chunk_overlap = 256,
        length_function = len,
        add_start_index = True,)
    chunks = separate.split_documents(docs)
    print("finished chunck process")
    return chunks

#Embedding com batches para não ter problemas com timeout no hugging face
def vetorize_chunks(chunks):
    print("starting vetorize process")
    embedding = HuggingFaceEmbeddings(model_name="google/embeddinggemma-300m",  model_kwargs={"token": HF_TOKEN})
    batch_size = 500

    first_batch = chunks[:batch_size]
    total_batch = len(chunks)
    print(f"total batches {total_batch}")
    db = Chroma.from_documents(
        documents=first_batch,
        embedding=embedding,
        persist_directory=persist_directory
    )
    print(f"first batch complete...")

    print("Waiting 10 seconds...")
    time.sleep(10)

    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        print(f"Processing chunks {i} to {i + len(batch)}...")
        db.add_documents(batch)
        print(f"Total no DB agora: {db._collection.count()}")
        print("Going next")
        

    print("finished vetorize process")
    return db

if __name__ == "__main__":
    kb = load_txt(kb_path)
    create_db(kb)