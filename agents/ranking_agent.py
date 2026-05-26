import re

from llm import call_llm


class RankingAgent:

    def run(self, user_input, flats):

        if not flats:
            return []

        flats_text = "\n".join([
            f"{i}. {f['rooms']}к, {f['price']}₽, метро {f['metro']}"
            for i, f in enumerate(flats)
        ])

        prompt = f"""
Пользователь:
{user_input}

Выбери ТОП-3 наиболее подходящих варианта.

Варианты:
{flats_text}

Верни только номера через запятую.

Пример:
0,1,2
"""

        result = call_llm(prompt)

        try:

            indexes = [int(x) for x in re.findall(r"\d+", result)]

            return [
                flats[i]
                for i in indexes
                if i < len(flats)
            ]

        except:
            return flats[:3]