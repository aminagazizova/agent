import requests
import json
import re

def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 120  
            }
        }
    )
    return response.json()["response"]


class QueryAgent:
    def run(self, user_input):
        prompt = f"""
Ты извлекаешь параметры недвижимости.

Верни ТОЛЬКО JSON:
rooms (int или null)
max_price (int или null)
metro (string или null)

Запрос: {user_input}
"""

        result = call_llm(prompt)

        try:
            import re
            import json

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
            print("QueryAgent error raw:", result)
            print("reason:", e)
            return {}

class SearchAgent:
    def run(self, params):
        with open("flats.json", "r", encoding="utf-8") as f:
            flats = json.load(f)

        results = []

        for flat in flats:
            score = 0

            if "rooms" in params and flat["rooms"] == params["rooms"]:
                score += 1

            if "max_price" in params and flat["price"] <= params["max_price"]:
                score += 1

            if "metro" in params and params.get("metro"):
                if params["metro"].lower() in flat["metro"].lower():
                    score += 1

            if score > 0:
                flat["score"] = score
                results.append(flat)

        return sorted(results, key=lambda x: x["score"], reverse=True)


class RankingAgent:
    def run(self, user_input, flats):
        if not flats:
            return []

        flats_text = "\n".join([
            f"{i}. {f['rooms']}к, {f['price']}₽, метро {f['metro']}"
            for i, f in enumerate(flats)
        ])

        prompt = f"""
Пользователь: {user_input}

Оцени варианты и выбери топ-3 (по номерам).

{flats_text}

Ответ: список номеров через запятую
Пример: 0,2,1
"""

        result = call_llm(prompt)

        try:
            indexes = [int(x) for x in re.findall(r"\d+", result)]
            return [flats[i] for i in indexes if i < len(flats)]
        except:
            return flats[:3]


class ResponseAgent:
    def run(self, user_input, flats):
        if not flats:
            return "Ничего не найдено."

        flats_text = "\n".join([
            f"{f['rooms']}к, {f['price']}₽, метро {f['metro']}: {f['description']}"
            for f in flats
        ])

        prompt = f"""
Ты — ассистент по недвижимости.

ВАЖНО:
- Отвечай ТОЛЬКО на русском языке
- НЕ используй английский
- Пиши кратко и понятно

Пользователь: {user_input}

Варианты:
{flats_text}

Объясни, почему они подходят.
"""

        return call_llm(prompt)