import operator
from typing import Annotated, TypedDict

class QueryState(TypedDict):
    input: str          
    query: str | None          
    validated_query: str | None  
    results: str | list | None   
    answer: str | None        
    intermediate_steps: Annotated[list[tuple[str, str]], operator.add]  
