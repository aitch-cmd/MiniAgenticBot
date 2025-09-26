from agents.states import QueryState
from core.llm import llm
from core.prompts import intent_classification_prompt

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