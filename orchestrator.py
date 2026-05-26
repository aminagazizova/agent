from agents.query_agent import QueryAgent
from agents.search_agent import SearchAgent
from agents.ranking_agent import RankingAgent
from agents.response_agent import ResponseAgent
from agents.dialog_agent import DialogAgent

from memory.memory import add_to_memory

from logger import logger


class Orchestrator:

    def __init__(self):

        self.query_agent = QueryAgent()

        self.search_agent = SearchAgent()

        self.ranking_agent = RankingAgent()

        self.response_agent = ResponseAgent()

        self.dialog_agent = DialogAgent()

    def run(self, user_input):

        logger.info(f"USER: {user_input}")

        params = self.query_agent.run(user_input)

        logger.info(f"PARAMS: {params}")

        clarification = self.dialog_agent.run(params)

        if clarification:

            logger.info(f"CLARIFICATION: {clarification}")

            return clarification

        flats = self.search_agent.run(params)

        logger.info(f"FOUND: {len(flats)}")

        if len(flats) > 5:

            ranked = self.ranking_agent.run(
                user_input,
                flats
            )

        else:
            ranked = flats[:3]

        answer = self.response_agent.run(
            user_input,
            ranked
        )

        add_to_memory(user_input, answer)

        logger.info(f"ANSWER: {answer}")

        return answer