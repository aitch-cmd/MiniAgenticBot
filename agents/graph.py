from agents.nodes import query_generation_node, query_validation_node, execute_query_node, result_formatting_node
from agents.states import QueryState
from core.llm import llm
from langgraph.graph import END, StateGraph

QUERY_GENERATION_NODE="query_generation_node"
QUERY_VALIDATION_NODE="query_validation_node"
EXECUTE_QUERY_NODE="execute_query_node"
RESULT_FORMATTING_NODE="result_formatting_node"

# Define the state graph
graph=StateGraph(QueryState)

# Defining nodes
graph.add_node(QUERY_GENERATION_NODE, query_generation_node)
graph.set_entry_point(QUERY_GENERATION_NODE)

graph.add_node(QUERY_VALIDATION_NODE, query_validation_node)
graph.add_node(EXECUTE_QUERY_NODE, execute_query_node)
graph.add_node(RESULT_FORMATTING_NODE, result_formatting_node)

# Defining edges
graph.add_edge(QUERY_GENERATION_NODE, QUERY_VALIDATION_NODE)
graph.add_edge(QUERY_VALIDATION_NODE, EXECUTE_QUERY_NODE)
graph.add_edge(EXECUTE_QUERY_NODE, RESULT_FORMATTING_NODE)
graph.add_edge(RESULT_FORMATTING_NODE, END)

app = graph.compile()

result = app.invoke(
    {
        "input": "What is the product purchased by Lisa Anderson?", 
        "query": None, 
        "validated_query": None, 
        "results": None,
        "intermediate_steps": []
    }
)

print("Validated Query:")
print(result.get('validated_query'))
print("\nFinal Answer:")
print(result.get('answer'))