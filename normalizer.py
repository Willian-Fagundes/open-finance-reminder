import json
import os
import yaml
from docx import Document
import pandas as pd
from pathlib import Path
from pypdf import PdfReader

destino = Path("/workspaces/open-finance-reminder/docs_processed")
root = Path.cwd()

arquivos_pdf = list(root.glob("**/*.pdf"))
arquivos_csv = list(root.glob("**/*.csv"))
arquivos_yml = list(root.glob("**/*.yml"))
arquivos_docx = list(root.glob("**/*.docx"))

def save_json(dados, origin_path, destiny_path):

    os.makedirs(destiny_path, exist_ok=True)

    nome_json = os.path.splitext(os.path.basename(origin_path))[0] + ".json"

    caminho_json = os.path.join(destiny_path, nome_json)

    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    return caminho_json


def pdf_to_json(origin_path, destiny_path):
    reader = PdfReader(origin_path)
    dados_pdf = {"arquivo_origem" : os.path.basename(origin_path),
                 "pages" : []}

    for numero, page in enumerate(reader.pages, start = 1):
        texto = page.extract_text()
        dados_pdf["pages"].append({
            "pagina": numero,
            "conteudo": texto
        })

    return save_json(dados_pdf,origin_path, destiny_path)
    
def yml_to_json(yml_path, destiny_path):
    with open(yml_path, "r", encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo)

    return save_json(
        dados,
        yml_path,
        destiny_path
    )


def csv_to_json(caminho_csv, destiny_path):
    tabela = pd.read_csv(caminho_csv, sep = ";")

    dados = tabela.to_dict(
        orient="records"
    )

    return save_json(
        dados,
        caminho_csv,
        destiny_path
    )

def docx_to_json(caminho_docx, destiny_path):
    documento = Document(caminho_docx)

    paragrafos = []

    for paragrafo in documento.paragraphs:
        if paragrafo.text.strip():
            paragrafos.append(
                paragrafo.text
            )

    dados = {
        "arquivo_original": os.path.basename(caminho_docx),
        "conteudo": paragrafos
    }

    return save_json(
        dados,
        caminho_docx,
        destiny_path
    )




for arquivo in arquivos_pdf:
    try:
        pdf_json = pdf_to_json(arquivo, destino)
        print(f"Convertido: {pdf_json}")
    except Exception as erro:
        print(f"Erro ao processar {arquivo}: {erro}") 

for arquivo in arquivos_yml:
    try:
        yml_json = yml_to_json(arquivo, destino)
        print(f"Convertido: {yml_json}")
    except Exception as erro:
        print(f"Erro ao processar {arquivo}: {erro}") 

for arquivo in arquivos_csv:
    try:
        csv_json = csv_to_json(arquivo, destino)
        print(f"Convertido: {csv_json}")
    except Exception as erro:
        print(f"Erro ao processar {arquivo}: {erro}") 

for arquivo in arquivos_docx:
    try:
        docx_json = docx_to_json(arquivo, destino)
        print(f"Convertido: {docx_json}")
    except Exception as erro:
        print(f"Erro ao processar {arquivo}: {erro}") 

