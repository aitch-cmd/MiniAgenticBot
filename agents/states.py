import operator
from typing import Annotated, TypedDict, Union, Literal

class QueryState(TypedDict):
    input: str
    intent: Literal["read", "create", "update", "delete"] | None
    query: str | None
    validated_query: str | None
    results: str | list | None
    answer: str | None
    human_verified: bool | None
    verification_required: bool
    intermediate_steps: Annotated[list[tuple[str, str]], operator.add]
