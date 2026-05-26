from typing import TypedDict, List


class AgentState(TypedDict):

    user_input: str

    params: dict

    flats: list

    ranked: list

    answer: str

    clarification: str