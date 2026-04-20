from agents import QueryAgent, SearchAgent, RankingAgent, ResponseAgent
from memory import add_to_memory

class Orchestrator:
    def __init__(self):
        self.query_agent = QueryAgent()
        self.search_agent = SearchAgent()
        self.ranking_agent = RankingAgent()
        self.response_agent = ResponseAgent()

    def run(self, user_input):
        print("Запуск агентов...")

        params = self.query_agent.run(user_input)
        print("Параметры:", params)

        flats = self.search_agent.run(params)

        if len(flats) > 5:
            print("Используем LLM для ranking (много вариантов)")
            ranked = self.ranking_agent.run(user_input, flats)
        else:
            print("Быстрый режим (без LLM ranking)")
            ranked = flats[:3]

        answer = self.response_agent.run(user_input, ranked)

        add_to_memory(user_input, answer)

        return answer


def main():
    orchestrator = Orchestrator()

    print("Мультиагентная система (Ollama)\n")

    while True:
        user_input = input("Ты: ")

        if user_input.lower() == "exit":
            break

        answer = orchestrator.run(user_input)

        print("\n🤖 Агент:\n", answer, "\n")


if __name__ == "__main__":
    main()