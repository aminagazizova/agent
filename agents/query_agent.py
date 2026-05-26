import json
import re

from llm import call_llm


class QueryAgent:

    def run(self, user_input):

        prompt = f"""
Ты извлекаешь параметры недвижимости.

Верни ТОЛЬКО JSON.

Формат:

{{
    "rooms": int|null,
    "max_price": int|null,
    "metro": string|null
}}

Никакого текста.

Запрос:
{user_input}
"""

        result = call_llm(prompt)

        try:

            json_str = re.search(r"\{[\s\S]*\}", result).group(0)

            data = json.loads(json_str)

            clean = {}

            if data.get("rooms") is not None:
                clean["rooms"] = int(data["rooms"])

            if data.get("max_price") is not None:
                clean["max_price"] = int(data["max_price"])

            if data.get("metro"):
                clean["metro"] = data["metro"]

            return clean

        except Exception as e:
            print("QueryAgent error:", e)
            print(result)

            return {}