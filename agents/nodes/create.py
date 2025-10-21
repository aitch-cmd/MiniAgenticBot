import sqlite3
from agents.states import QueryState
from core.llm import llm
from core.prompts import create_query_generation_prompt, create_query_validation_prompt, create_result_formatting_prompt, schema
from agents.nodes.read import strip_sql_code_fences

def create_query_generation_node(state: QueryState) -> QueryState:
    input_text = state.get("input")
    generated_query = llm.invoke(create_query_generation_prompt.format(input=input_text, schema=schema))
    query = generated_query.content if hasattr(generated_query, 'content') else str(generated_query)
    state["query"] = query
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("create_query_generation", query))
    state["intermediate_steps"] = intermediate
    return state

def create_query_validation_node(state: QueryState) -> QueryState:
    query = state.get("query")
    input_text = state.get('input')
    validated_query = llm.invoke(create_query_validation_prompt.format(input=input_text, query=query, schema=schema))
    validated_query_str = validated_query.content if hasattr(validated_query, 'content') else str(validated_query)
    state["validated_query"] = validated_query_str
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("create_query_validation", validated_query_str))
    state["intermediate_steps"] = intermediate
    return state

def create_human_verification_node(state: QueryState) -> QueryState:
    # If human_verified is already set (from frontend), skip prompt logic
    if state.get("human_verified") is not None:
        # Approval has already been given by frontend, just document it
        state["verification_required"] = False  # Clear the flag since approval is handled
        state["intermediate_steps"].append(
            ("human_verification", str(state["human_verified"]))
        )
        return state

    state["verification_required"] = True
    state["human_verified"] = None  # Not yet approved or declined
    state["intermediate_steps"].append(("human_verification", "pending"))
    return state

def execute_query_create_node(state: QueryState) -> QueryState:
    if not state.get("human_verified", False):
        state["results"] = "Create operation was not approved."
    else:
        query = state.get("validated_query")
        # Ensure query is a clean string
        query = query.content if hasattr(query, "content") else str(query)
        query = strip_sql_code_fences(query)
        results = None
        try:
            conn = sqlite3.connect("data/apps.db")
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            conn.close()
            results = "Row inserted successfully."
        except Exception as e:
            results = str(e)
        state["results"] = results
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("execute_create", str(state["results"])))
    state["intermediate_steps"] = intermediate
    return state

def create_result_formatting_node(state: QueryState) -> QueryState:
    results = state.get('results')
    formatted_answer = llm.invoke(create_result_formatting_prompt.format(results=results))
    answer_content = formatted_answer.content if hasattr(formatted_answer, 'content') else str(formatted_answer)
    state["answer"] = answer_content
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("result_formatting", answer_content))
    state["intermediate_steps"] = intermediate
    return state
