import os
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup

url_base = "https://openfinancebrasil.atlassian.net"

def search_page_links(url_base):
    with open("./data/links_op.json", "r") as file:
            url_list = json.load(file)
    url_visitados = {item["link"] for item in url_list}
    for data in url_list:
        link = data["link"]

        if not link.startswith("https") and not link.startswith("http"):

            url_busca = url_base + link
            try:
                response = requests.get(url_busca)
                html_doc = response.text
                soup = BeautifulSoup(html_doc, "html.parser")
                content = soup.find_all("href") or soup.find_all("a")

                for tag in content:
                    page_title = tag.get_text(strip=True) or "Sem título"
                    link_href = tag.get("href")
                    
                    if link_href not in url_visitados and not link_href.startswith("#"):
                        url_list.append({"title" : page_title, "link" : link_href})
                        url_visitados.add(link_href)
                        print(f"Visitado -> Title : {page_title} Link : {link_href}")
                save_json(url_list)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    save_json(url_list)
                    print("No more links or request error")
        
def save_json(new_data):

    root_folder = Path("/workspaces/open-finance-reminder/data")
    filename = "links_op.json"

    os.makedirs(root_folder, exist_ok = True)
    filepath = os.path.join(root_folder, filename)

    with open (filepath, "r") as file:
        existing_links = json.load(file)

    if not existing_links:
        existing_links = new_data

    merged_links = {item["title"]: item for item in existing_links + new_data}
    final_links = list(merged_links.values())
    
    with open(filepath, "w") as file:
        json.dump(final_links, file, indent=4, ensure_ascii=False)

def save_text_file(title, content):
    root_folder = Path("/workspaces/open-finance-reminder/data")
    filename = "knowledge_base.txt"

    os.makedir(root_folder, exist_ok = True)
    filepath = os.path.join(root_folder, filename)

    with open(filepath, "a", encoding = "utf-8") as file:
        file.write(title + "\n")
        file.write(content)

#Boa parte dos links coletados seguem o formato "/wiki/spaces/OF/"conteudo" preciso fazer com que seja concatenado com o link url_base para alcnaçar todo o conteudo da pagina
def extract_text(url_base):
    wiki_links = "/wiki/spaces/OF/"
    
    with open("links_op.json", "r") as file:
        url_list = json.load(file)

    url_to_go = len(url_list)
    url_count = 0
    sucesso = 0
    falha = 0
    try:
        for data in url_list:
            doc_title = data["title"]
            link = data["link"]
            print(f"Link atual -> {doc_title}")
            if link.startswith(wiki_links):
                url_busca = url_base + link
            else:
                url_busca = link
            try:
                html_doc = requests.get(url_busca).text
                soup = BeautifulSoup(html_doc, "html.parser")
                for p in soup.find_all("p"):
                    content = p.get_text(separator="\n", strip=True)
                    save_text_file(doc_title, content)
                sucesso += 1
            except Exception as e:
                print(f"Erro em {url_busca}")
                print(type(e).__name__, e)
                url_to_go -= 1
                falha += 1
                continue

            url_count += 1
            url_to_go -= 1
            print(f"Total url [{url_count}]\nUrl to go [{url_to_go}]")
            print(f"Bem sucedidas [{sucesso}], Falhas [{falha}]")
    except Exception as e:
                    print(f"Erro em {url_busca}")
                    print(type(e).__name__, e)

search_page_links(url_base)