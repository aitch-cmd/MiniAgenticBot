import sqlite3
from agents.states import QueryState
from core.llm import llm
from core.prompts import query_generation_prompt, query_validation_prompt, result_formatting_prompt

def query_generation_node(state: QueryState) -> QueryState:
    # Get the user input
    input_text = state.get('input')
    sql_query = llm.invoke(query_generation_prompt.format(input=input_text))
    # Update state
    state["query"] = sql_query
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("query_generation", sql_query))
    state["intermediate_steps"] = intermediate
    return state


def execute_query_node(state: QueryState) -> QueryState:
    query = state.get('validated_query')
    results = None
    try:
        conn = sqlite3.connect("data/app.db")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
    except Exception as e:
        results = str(e)
    # Add the intermediate step to the state
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("execute_query", str(results)))
    state["results"] = results
    state["intermediate_steps"] = intermediate
    return state

def query_validation_node(state: QueryState) -> QueryState:
    query = state.get('query')
    validated_query = llm.invoke(query_validation_prompt.format(query=query))
    # Update state
    state["validated_query"] = validated_query
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("query_validation", validated_query))
    state["intermediate_steps"] = intermediate
    return state

def result_formatting_node(state: QueryState) -> QueryState:
    results = state.get('results')
    formatted_answer = llm.invoke(result_formatting_prompt.format(results=results))
    # Update state
    state["answer"] = formatted_answer
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("result_formatting", formatted_answer))
    state["intermediate_steps"] = intermediate
    return state