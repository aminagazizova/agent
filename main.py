from graph.workflow import app


def main():

    print("LangGraph Real Estate AI\n")

    while True:

        user_input = input("Ты: ")

        if user_input.lower() == "exit":
            break

        result = app.invoke({
            "user_input": user_input
        })

        print("\nAI:\n")

        print(result["answer"])

        print()


if __name__ == "__main__":
    main()