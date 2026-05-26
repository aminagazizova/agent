from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.query_agent import QueryAgent
from agents.search_agent import SearchAgent
from agents.ranking_agent import RankingAgent
from agents.response_agent import ResponseAgent
from agents.dialog_agent import DialogAgent


query_agent = QueryAgent()

search_agent = SearchAgent()

ranking_agent = RankingAgent()

response_agent = ResponseAgent()

dialog_agent = DialogAgent()


def query_node(state: AgentState):

    params = query_agent.run(
        state["user_input"]
    )

    state["params"] = params

    return state


def dialog_node(state: AgentState):

    clarification = dialog_agent.run(
        state["params"]
    )

    state["clarification"] = clarification

    return state


# ROUTER

def dialog_router(state: AgentState):

    if state["clarification"]:
        return "need_clarification"

    return "continue_search"


def search_node(state: AgentState):

    flats = search_agent.run(
        state["params"]
    )

    state["flats"] = flats

    return state


def ranking_node(state: AgentState):

    ranked = ranking_agent.run(
        state["user_input"],
        state["flats"]
    )

    state["ranked"] = ranked

    return state


def response_node(state: AgentState):

    answer = response_agent.run(
        state["user_input"],
        state["ranked"]
    )

    state["answer"] = answer

    return state


def clarification_node(state: AgentState):

    state["answer"] = state["clarification"]

    return state


workflow = StateGraph(AgentState)


workflow.add_node(
    "query",
    query_node
)

workflow.add_node(
    "dialog",
    dialog_node
)

workflow.add_node(
    "search",
    search_node
)

workflow.add_node(
    "ranking",
    ranking_node
)

workflow.add_node(
    "response",
    response_node
)

workflow.add_node(
    "clarification",
    clarification_node
)

workflow.set_entry_point("query")

workflow.add_edge(
    "query",
    "dialog"
)


workflow.add_conditional_edges(
    "dialog",
    dialog_router,
    {
        "need_clarification": "clarification",
        "continue_search": "search"
    }
)


workflow.add_edge(
    "search",
    "ranking"
)

workflow.add_edge(
    "ranking",
    "response"
)

workflow.add_edge(
    "response",
    END
)

workflow.add_edge(
    "clarification",
    END
)


app = workflow.compile()