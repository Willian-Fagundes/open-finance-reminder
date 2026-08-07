from src.graph import graph

result = graph.invoke(
    {
        "question": 
        "o que é consent stock ?"
    })


print(result["final_answer"])