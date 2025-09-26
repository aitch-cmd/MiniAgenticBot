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

def query_validation_node(state: QueryState) -> QueryState:
    query = state.get('query')
    validated_query_obj = llm.invoke(query_validation_prompt.format(query=query))
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


def execute_query_node(state: QueryState) -> QueryState:
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

def result_formatting_node(state: QueryState) -> QueryState:
    results = state.get('results')
    formatted_answer = llm.invoke(result_formatting_prompt.format(results=results))
    
    if hasattr(formatted_answer, 'content'):
        answer_content = formatted_answer.content
    else:
        answer_content = str(formatted_answer)
    
    state["answer"] = answer_content
    intermediate = state.get('intermediate_steps', [])
    intermediate.append(("result_formatting", answer_content))
    state["intermediate_steps"] = intermediate

    return state