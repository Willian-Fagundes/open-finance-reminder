from ddgs import DDGS

def search_web(query, max_results = 4) -> list:
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, regions = "br-pt", max_results = max_results)]
        return results
    

def open_md(filename):
    path = "./prompts/"
    filepath = path + filename
    with open(filepath, "r", encoding="utf-8") as file:
        prompt_system = file.read()
    return prompt_system