class DialogAgent:

    def run(self, params):

        if "rooms" not in params:
            return "Сколько комнат вам нужно?"

        if "metro" not in params:
            return "Какой район или метро вас интересует?"

        return None