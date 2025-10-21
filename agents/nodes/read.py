import sqlite3
from agents.states import QueryState
from core.llm import llm
from core.prompts import intent_classification_prompt, read_query_generation_prompt, read_query_validation_prompt, read_result_formatting_prompt, schema

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

def read_query_generation_node(state: QueryState) -> QueryState:
    # Get the user input
    input_text = state.get('input')
    sql_query = llm.invoke(read_query_generation_prompt.format(input=input_text, schema=schema))
    # Update state
    state["query"] = sql_query
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("query_generation", sql_query))
    state["intermediate_steps"] = intermediate
    return state

def read_query_validation_node(state: QueryState) -> QueryState:
    query = state.get('query')
    input_text = state.get('input')
    validated_query_obj = llm.invoke(read_query_validation_prompt.format(input=input_text, query=query, schema=schema))
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
        conn = sqlite3.connect("data/apps.db")
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
