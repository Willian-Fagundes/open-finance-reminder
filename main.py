import yaml
import time
import os
import json
import traceback
import pandas as pd
from pypdf import PdfReader
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_chroma.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.environ.get("HF_TOKEN")

BASE_DIR = Path("/workspaces/open-finance-reminder")

persist_directory = str(BASE_DIR / "agents" / "DB")

root = Path("/workspaces/open-finance-reminder/docs_raw")

yaml_paths = list(root.glob("**/*.yaml")) + list(root.glob("**/*.yml"))
pdf_paths = list(root.glob("**/*.pdf"))
json_paths = list(root.glob("**/*.json"))


def create_db():
    print("starting db process")
    pdf_docs = load_pdf(pdf_paths)
    yaml_docs = load_yaml(yaml_paths)
    json_docs = load_json(json_paths)
    all_docs = pdf_docs + yaml_docs + json_docs

    chunks = chunk_data(all_docs)
    vetorize_chunks(chunks)
    print("finishing db process")

def chunk_data(docs):
    print("starting chunck process")
    separate = RecursiveCharacterTextSplitter(
        chunk_size = 512,
        chunk_overlap = 64,
        length_function = len,
        add_start_index = True,)
    chunks = separate.split_documents(docs)
    print("finished chunck process")
    return chunks

def vetorize_chunks(chunks):
    print("starting vetorize process")
    embedding = HuggingFaceEmbeddings(model_name="google/embeddinggemma-300m",  model_kwargs={"token": HF_TOKEN})
    batch_size = 100

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

def load_yaml(yaml_paths):
    print("loading yaml")
    docs = []
    for path in yaml_paths:
        with path.open("r", encoding="utf-8") as file:
            content = yaml.safe_load(file)

        paths_section = content.get("paths", {})
        if paths_section:
            for endpoint, methods in paths_section.items():
                for method, details in methods.items():
                    texto = yaml.dump({endpoint: {method: details}}, allow_unicode=True, sort_keys=False)
                    docs.append(Document(
                        page_content=texto,
                        metadata={
                            "arquivo_origem": os.path.basename(path),
                            "tipo": "yaml",
                            "endpoint": endpoint,
                            "method": method
                        }
                    ))
        else:
            texto = yaml.dump(content, allow_unicode=True, sort_keys=False)
            docs.append(Document(
                page_content=texto,
                metadata={"arquivo_origem": os.path.basename(path), "tipo": "yaml"}
            ))
    print("complete")
    return docs

def load_pdf(pdf_paths):
    print("loading pdf")
    all_docs = []
    for pdf in pdf_paths:
        reader = PdfReader(pdf)
        for numero, page in enumerate(reader.pages, start=1):
            texto = page.extract_text() or ""
            all_docs.append(Document(
                page_content=texto,
                metadata={"arquivo_origem": os.path.basename(pdf), "pagina": numero}
            ))
    print("complete")
    return all_docs

def load_json(json_paths):
    print("loading json")
    docs = []

    for path in json_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            for index, item in enumerate(data):
                docs.append(
                    Document(
                        page_content=json.dumps(
                            item,
                            ensure_ascii=False,
                            indent=2
                        ),
                        metadata={
                            "arquivo_origem": path.name,
                            "tipo": "json",
                            "index": index,
                        },
                    )
                )

        elif isinstance(data, dict):
            docs.append(
                Document(
                    page_content=json.dumps(
                        data,
                        ensure_ascii=False,
                        indent=2
                    ),
                    metadata={
                        "arquivo_origem": path.name,
                        "tipo": "json",
                    },
                )
            )

        else:
            docs.append(
                Document(
                    page_content=str(data),
                    metadata={
                        "arquivo_origem": path.name,
                        "tipo": "json",
                    },
                )
            )

    print("complete")
    return docs

if __name__ == "__main__":
    create_db()