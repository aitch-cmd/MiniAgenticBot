import sqlite3
from agents.states import QueryState
from core.llm import llm
from core.prompts import update_query_generation_prompt, update_query_validation_prompt, update_result_formatting_prompt
from agents.nodes.read import strip_sql_code_fences

def update_query_generation_node(state: QueryState) -> QueryState:
    input_text = state.get("input")
    generated_query = llm.invoke(update_query_generation_prompt.format(input=input_text))
    query = generated_query.content if hasattr(generated_query, 'content') else str(generated_query)
    state["query"] = query
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("update_query_generation", query))
    state["intermediate_steps"] = intermediate
    return state

def update_query_validation_node(state: QueryState) -> QueryState:
    query = state.get("query")
    input_text = state.get('input')
    validated_query = llm.invoke(update_query_validation_prompt.format(input=input_text, query=query))
    validated_query_str = validated_query.content if hasattr(validated_query, 'content') else str(validated_query)
    state["validated_query"] = validated_query_str
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("update_query_validation", validated_query_str))
    state["intermediate_steps"] = intermediate
    return state

def update_human_verification_node(state: QueryState) -> QueryState:
    print("Do you approve the following UPDATE operation?\n", state["validated_query"])
    response = input("Approve? (yes/no): ")  
    state["human_verified"] = response.strip().lower() == "yes"
    state["intermediate_steps"].append(("human_verification", str(state["human_verified"])))
    return state

def execute_query_update_node(state: QueryState) -> QueryState:
    if not state.get("human_verified", False):
        state["results"] = "Update operation was not approved."
    else:
        query = state.get("validated_query")
        query = query.content if hasattr(query, "content") else str(query)
        query = strip_sql_code_fences(query)
        try:
            conn = sqlite3.connect("data/apps1.db")
            c = conn.cursor()
            c.execute(query)
            affected = c.rowcount 
            conn.commit()
            conn.close()
            results = f"Row(s) updated successfully. ({affected} affected)" 
        except Exception as e:
            results = str(e)
        state["results"] = results
    if "intermediate_steps" not in state or state["intermediate_steps"] is None:
        state["intermediate_steps"] = []
    state["intermediate_steps"].append(("execute_update", str(state["results"])))
    return state

def update_result_formatting_node(state: QueryState) -> QueryState:
    results = state.get('results')
    formatted_answer = llm.invoke(update_result_formatting_prompt.format(results=results))
    answer_content = formatted_answer.content if hasattr(formatted_answer, 'content') else str(formatted_answer)
    state["answer"] = answer_content
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("result_formatting", answer_content))
    state["intermediate_steps"] = intermediate
    return state

