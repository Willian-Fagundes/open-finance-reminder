import json
import os
import yaml
from docx import Document
import pandas as pd
from pathlib import Path
from pypdf import PdfReader

destino = Path("/workspaces/open-finance-reminder/docs_processed")
root = Path("/workspaces/open-finance-reminder/docs_raw")

arquivos_pdf = list(root.glob("**/*.pdf"))
arquivos_csv = list(root.glob("**/*.csv"))
arquivos_yml = list(root.glob("**/*.yml"))
arquivos_docx = list(root.glob("**/*.docx"))




