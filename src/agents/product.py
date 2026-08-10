from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from state import AgentState
from src.models import gpt_groq
from src.utils import open_md, search_web

PM_PROMPT = open_md("product.md")

prompt = ChatPromptTemplate.from_messages([
    ("system", PM_PROMPT),("human","contexto da documentação:{context}"),])

llm = gpt_groq()
pm_chain = (prompt | llm | JsonOutputParser())


def format_document_list(documents):
    return "\n\n".join([
        f"Título: {doc.get('metadata', {}).get('title', '')}\nFonte: {doc.get('metadata', {}).get('source', '')}\n{doc.get('content', '')}"
        for doc in documents
    ])


def format_search_results(results):
    return "\n\n".join([
        f"Título: {result.get('title', '')}\nFonte: {result.get('href') or result.get('url') or result.get('source', '')}\n{result.get('body') or result.get('text') or result.get('snippet') or ''}"
        for result in results
    ])


def pm_agent_node(state: AgentState):
    confidence = state.get("confidence", 0.0)
    kb_documents = state["researcher_output"]["documents"]
    context_parts = []

    if confidence < 0.7:
        web_results = search_web(state["question"], max_results=4)
        web_context = format_search_results(web_results)

        if confidence < 0.5:
            context_parts.append(
                "Use a pesquisa web como fonte principal para esta resposta. Priorize o conteúdo obtido pela pesquisa na web ao construir a explicação final."
            )
            context_parts.append(
                "Use também a documentação local disponível como contexto adicional, mas mantenha o foco nos resultados de pesquisa web."
            )
            if web_context:
                context_parts.append("Resultados da pesquisa web prioritários:\n\n" + web_context)
            if kb_documents:
                context_parts.append("Contexto adicional da documentação local:\n\n" + format_document_list(kb_documents))
        else:
            context_parts.append(
                "Use a documentação local como base e complemente com a pesquisa web para responder com maior precisão."
            )
            if kb_documents:
                context_parts.append("Documentação local encontrada:\n\n" + format_document_list(kb_documents))
            if web_context:
                context_parts.append("Pesquisa complementar na internet:\n\n" + web_context)
    else:
        if kb_documents:
            context_parts.append("Documentação local encontrada:\n\n" + format_document_list(kb_documents))
    context = "\n\n".join(context_parts) if context_parts else "Nenhuma documentação ou resultado de pesquisa disponível."
    result = pm_chain.invoke({"context": context})

    return {"product_output": result}