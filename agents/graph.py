from .nodes.react import reason_and_act_node
from .nodes.read import read_query_generation_node, read_query_validation_node, execute_query_read_node, read_result_formatting_node
from .nodes.create import create_query_generation_node, create_query_validation_node, create_human_verification_node, execute_query_create_node, create_result_formatting_node
from .nodes.update import update_query_generation_node, update_query_validation_node, update_human_verification_node, execute_query_update_node, update_result_formatting_node
from .nodes.delete import delete_query_generation_node, delete_query_validation_node, delete_human_verification_node, execute_query_delete_node, delete_result_formatting_node
from agents.states import QueryState
from core.llm import llm
from langgraph.graph import END, StateGraph

# QUERY CLASSIFICATION
REASON_AND_ACT_NODE = "reason_and_act_node"

# READ
QUERY_GENERATION_NODE = "query_generation_node"
QUERY_VALIDATION_NODE = "query_validation_node"
EXECUTE_QUERY_NODE = "execute_query_node"
RESULT_FORMATTING_NODE = "result_formatting_node"

# CREATE
CREATE_QUERY_GENERATION_NODE = "create_query_generation_node"
CREATE_QUERY_VALIDATION_NODE = "create_query_validation_node"
CREATE_HUMAN_VERIFICATION_NODE = "create_human_verification_node"
EXECUTE_QUERY_CREATE_NODE = "execute_query_create_node"
CREATE_RESULT_FORMATTING_NODE = "create_result_formatting_node"

# UPDATE
UPDATE_QUERY_GENERATION_NODE = "update_query_generation_node"
UPDATE_QUERY_VALIDATION_NODE = "update_query_validation_node"
UPDATE_HUMAN_VERIFICATION_NODE = "update_human_verification_node"
EXECUTE_QUERY_UPDATE_NODE = "execute_query_update_node"
UPDATE_RESULT_FORMATTING_NODE = "update_result_formatting_node"

# DELETE
DELETE_QUERY_GENERATION_NODE = "delete_query_generation_node"
DELETE_QUERY_VALIDATION_NODE = "delete_query_validation_node"
DELETE_HUMAN_VERIFICATION_NODE = "delete_human_verification_node"
EXECUTE_QUERY_DELETE_NODE = "execute_query_delete_node"
DELETE_RESULT_FORMATTING_NODE = "delete_result_formatting_node"

# Define the state graph
graph = StateGraph(QueryState)

# Defining nodes
graph.add_node(REASON_AND_ACT_NODE, reason_and_act_node)
graph.set_entry_point(REASON_AND_ACT_NODE)

# -----READ Nodes-----    
# Nodes
graph.add_node(QUERY_GENERATION_NODE, read_query_generation_node)
graph.add_node(QUERY_VALIDATION_NODE, read_query_validation_node)
graph.add_node(EXECUTE_QUERY_NODE, execute_query_read_node)
graph.add_node(RESULT_FORMATTING_NODE, read_result_formatting_node)

# -----CREATE Nodes-----
graph.add_node(CREATE_QUERY_GENERATION_NODE, create_query_generation_node)
graph.add_node(CREATE_QUERY_VALIDATION_NODE, create_query_validation_node)    
graph.add_node(CREATE_HUMAN_VERIFICATION_NODE, create_human_verification_node)
graph.add_node(EXECUTE_QUERY_CREATE_NODE, execute_query_create_node)
graph.add_node(CREATE_RESULT_FORMATTING_NODE, create_result_formatting_node)

# -----UPDATE Nodes-----
graph.add_node(UPDATE_QUERY_GENERATION_NODE, update_query_generation_node)
graph.add_node(UPDATE_QUERY_VALIDATION_NODE, update_query_validation_node)
graph.add_node(UPDATE_HUMAN_VERIFICATION_NODE, update_human_verification_node)
graph.add_node(EXECUTE_QUERY_UPDATE_NODE, execute_query_update_node)
graph.add_node(UPDATE_RESULT_FORMATTING_NODE, update_result_formatting_node)

# -----DELETE Nodes-----
graph.add_node(DELETE_QUERY_GENERATION_NODE, delete_query_generation_node)
graph.add_node(DELETE_QUERY_VALIDATION_NODE, delete_query_validation_node)
graph.add_node(DELETE_HUMAN_VERIFICATION_NODE, delete_human_verification_node)
graph.add_node(EXECUTE_QUERY_DELETE_NODE, execute_query_delete_node)
graph.add_node(DELETE_RESULT_FORMATTING_NODE, delete_result_formatting_node)

# Routing functions
def route_based_on_intent(state):
    """Route to different nodes based on intent"""
    intent = state.get("intent")
    if intent == "read":
        return QUERY_GENERATION_NODE
    elif intent == "create":
        return CREATE_QUERY_GENERATION_NODE
    elif intent == "update":
        return UPDATE_QUERY_GENERATION_NODE
    elif intent == "delete":
        return DELETE_QUERY_GENERATION_NODE
    return END

def route_human_verification(state):
    """Route based on human verification result"""
    human_verified = state.get("human_verified")
    if human_verified == True:
        return EXECUTE_QUERY_CREATE_NODE
    elif human_verified == False:
        return END
    return END

# Main routing from reason_and_act_node
graph.add_conditional_edges(REASON_AND_ACT_NODE, route_based_on_intent)

# READ flow edges
graph.add_edge(QUERY_GENERATION_NODE, QUERY_VALIDATION_NODE)
graph.add_edge(QUERY_VALIDATION_NODE, EXECUTE_QUERY_NODE)
graph.add_edge(EXECUTE_QUERY_NODE, RESULT_FORMATTING_NODE)
graph.add_edge(RESULT_FORMATTING_NODE, END)

# CREATE flow edges
graph.add_edge(CREATE_QUERY_GENERATION_NODE, CREATE_QUERY_VALIDATION_NODE)
graph.add_edge(CREATE_QUERY_VALIDATION_NODE, CREATE_HUMAN_VERIFICATION_NODE)
graph.add_conditional_edges(CREATE_HUMAN_VERIFICATION_NODE, route_human_verification)
graph.add_edge(EXECUTE_QUERY_CREATE_NODE, CREATE_RESULT_FORMATTING_NODE)
graph.add_edge(CREATE_RESULT_FORMATTING_NODE, END)

# UPDATE flow edges
graph.add_edge(UPDATE_QUERY_GENERATION_NODE, UPDATE_QUERY_VALIDATION_NODE)
graph.add_edge(UPDATE_QUERY_VALIDATION_NODE, UPDATE_HUMAN_VERIFICATION_NODE)
graph.add_conditional_edges(UPDATE_HUMAN_VERIFICATION_NODE, route_human_verification)
graph.add_edge(EXECUTE_QUERY_UPDATE_NODE, UPDATE_RESULT_FORMATTING_NODE)
graph.add_edge(UPDATE_RESULT_FORMATTING_NODE, END)

# DELETE flow edges
graph.add_edge(DELETE_QUERY_GENERATION_NODE, DELETE_QUERY_VALIDATION_NODE)
graph.add_edge(DELETE_QUERY_VALIDATION_NODE, DELETE_HUMAN_VERIFICATION_NODE)
graph.add_conditional_edges(DELETE_HUMAN_VERIFICATION_NODE, route_human_verification)
graph.add_edge(EXECUTE_QUERY_DELETE_NODE, DELETE_RESULT_FORMATTING_NODE)
graph.add_edge(DELETE_RESULT_FORMATTING_NODE, END)

app = graph.compile()

result = app.invoke(
    {
        "input": "Delete the product Iphone 17", 
        "intent": None,
        "query": None, 
        "validated_query": None, 
        "results": None,
        "answer": None,
        "human_verified": None,
        "intermediate_steps": []
    }
)

print("Validated Query:")
print(result.get('validated_query'))
print("\nFinal Answer:")
print(result.get('answer'))