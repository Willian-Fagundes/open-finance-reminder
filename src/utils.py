def open_md(filename):
    path = "./prompts/"
    filepath = path + filename
    with open(filepath, "r", encoding="utf-8") as file:
        prompt_system = file.read()
    return prompt_system