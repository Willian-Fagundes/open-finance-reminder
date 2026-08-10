# Open Finance Developer Intelligence

> Agente RAG especializado em Open Finance, capaz de recuperar documentações relevantes e auxiliar desenvolvedores na análise e adaptação de código para diferentes integrações e requisitos técnicos.



## Problema

A necessidade surgiu a partir de reclamações de uma desenvolvedora extramamente importante (minha esposa) que precisa consultar documentação técnica, interpretar requisitos específicos e adaptar códigos para diferentes integrações, mas encontra limitações e barreiras na própria documentação que por ser muito extensa demanda muito tempo para pesquisa.

O projeto busca solucionar esse problema por meio de um agente especializado em Open Finance, utilizando RAG para fundamentar suas respostas em documentação técnica relevante e auxiliar ela tanto na busca de informações quanto na adaptação de código e solução de bugs.

## Objetivos

O projeto tem como objetivo desenvolver um agente especializado em Open Finance capaz de:

Consultar documentação técnica e recuperar informações relevantes para cada solicitação.

Responder dúvidas técnicas com base nas fontes de conhecimento disponíveis.

Interpretar requisitos e especificações relacionados às integrações de Open Finance.

Analisar trechos de código fornecidos pelo desenvolvedor.

Sugerir adaptações de código de acordo com a documentação e os requisitos identificados.

Reduzir o tempo de pesquisa e implementação durante o desenvolvimento de integrações Open Finance.

## Arquitetura de IA

O projeto utiliza diferentes LLMs de acordo com a natureza de cada etapa do fluxo, buscando aproveitar as características de cada modelo:

**Llama**  — Orquestração: responsável por interpretar a solicitação, determinar o fluxo de execução e coordenar os diferentes agentes e ferramentas.

**Gemini / GPT** — Análise e adaptação de código: utilizados para tarefas que exigem maior capacidade de interpretação e geração de código, como análise de implementações existentes e sugestão de adaptações.

**Llama** — Sumarização: utilizado para consolidar as informações recuperadas e as respostas produzidas durante o fluxo, entregando uma resposta final mais objetiva ao desenvolvedor.

Essa abordagem permite distribuir diferentes responsabilidades entre os modelos, em vez de depender de uma única LLM para todo o processo.
