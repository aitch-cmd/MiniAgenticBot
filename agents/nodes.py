import sqlite3
from agents.states import QueryState
from core.llm import llm
from core.prompts import (intent_classification_prompt, read_query_generation_prompt, read_query_validation_prompt, read_result_formatting_prompt, create_query_generation_prompt, create_query_validation_prompt, create_result_formatting_prompt)

def reason_and_act_node(state: QueryState) -> QueryState:
    user_input = state.get("input")
    # Get the predicted intent from LLM
    intent_response = llm.invoke(intent_classification_prompt.format(input=user_input))
    intent_text = intent_response.content if hasattr(intent_response, "content") else str(intent_response)
    intent = intent_text.strip().lower()
    # Add step to intermediate_steps
    steps = state.get('intermediate_steps', [])
    steps.append(("intent_classification", intent))
    state['intent'] = intent
    state['intermediate_steps'] = steps
    return state

# -----READ-----
def read_query_generation_node(state: QueryState) -> QueryState:
    # Get the user input
    input_text = state.get('input')
    sql_query = llm.invoke(read_query_generation_prompt.format(input=input_text))
    # Update state
    state["query"] = sql_query
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("query_generation", sql_query))
    state["intermediate_steps"] = intermediate
    return state

def read_query_validation_node(state: QueryState) -> QueryState:
    query = state.get('query')
    validated_query_obj = llm.invoke(read_query_validation_prompt.format(query=query))
    # Extract raw string
    validated_query = (
        validated_query_obj.content if hasattr(validated_query_obj, "content") else validated_query_obj
    )
    # Optionally remove markdown formatting or extra code fences:
    if isinstance(validated_query, str):
        validated_query = validated_query.replace("``````", "").strip()
    state["validated_query"] = validated_query
    # Log and return
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("query_validation", validated_query))
    state["intermediate_steps"] = intermediate
    return state

def strip_sql_code_fences(sql: str) -> str:
    if not sql:
        return ""
    sql = sql.strip()
    
    # Remove triple backticks and optional 'sql' marker
    if sql.startswith("```sql"):
        sql = sql[len("```sql"):].strip()
    elif sql.startswith("```"):
        sql = sql[len("```"):].strip()
    
    if sql.endswith("```"):
        sql = sql[:-len("```")].strip()
    
    return sql


def execute_query_read_node(state: QueryState) -> QueryState:
    query = state.get('validated_query')
    if hasattr(query, "content"):
        query = query.content
    
    # Clean up any markdown
    query = strip_sql_code_fences(query)
    
    results = None
    try:
        conn = sqlite3.connect("data/app.db")
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        conn.close()
    except Exception as e:
        results = str(e)
    
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("execute_query", str(results)))
    state["results"] = results
    state["intermediate_steps"] = intermediate
    
    return state

def read_result_formatting_node(state: QueryState) -> QueryState:
    results = state.get('results')
    formatted_answer = llm.invoke(read_result_formatting_prompt.format(results=results))
    
    if hasattr(formatted_answer, 'content'):
        answer_content = formatted_answer.content
    else:
        answer_content = str(formatted_answer)
    
    state["answer"] = answer_content
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("result_formatting", answer_content))
    state["intermediate_steps"] = intermediate

    return state


# -----CREATE-----

def create_query_generation_node(state: QueryState) -> QueryState:
    input_text = state.get("input")

    generated_query = llm.invoke(create_query_generation_prompt.format(input=input_text))
    # Handle .content if needed
    query = generated_query.content if hasattr(generated_query, 'content') else str(generated_query)
    state["query"] = query
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("create_query_generation", query))
    state["intermediate_steps"] = intermediate
    return state

def create_query_validation_node(state: QueryState) -> QueryState:
    query = state.get("query")
    validated_query = llm.invoke(create_query_validation_prompt.format(query=query))
    validated_query_str = validated_query.content if hasattr(validated_query, 'content') else str(validated_query)
    state["validated_query"] = validated_query_str
    intermediate = state.get("intermediate_steps", [])
    intermediate.append(("create_query_validation", validated_query_str))
    state["intermediate_steps"] = intermediate
    return state

def create_human_verification_node(state: QueryState) -> QueryState:
    print("Do you approve the following operation?\n", state["validated_query"])
    response = input("Approve? (yes/no): ")  
    state["human_verified"] = response.strip().lower() == "yes"
    state["intermediate_steps"].append(("human_verification", str(state["human_verified"])))
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
            conn = sqlite3.connect("data/app.db")
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
