from llm import call_llm

from rag.rag import retrieve
from memory.memory import get_last_context


class ResponseAgent:

    def run(self, user_input, flats):

        if not flats:
            return "Ничего не найдено."

        rag_context = "\n".join(
            retrieve(user_input)
        )

        history = get_last_context()

        flats_text = "\n".join([
            f"""
{f['rooms']}к квартира
Цена: {f['price']}₽
Метро: {f['metro']}
Описание: {f['description']}
"""
            for f in flats
        ])

        prompt = f"""
Ты — AI ассистент по недвижимости.

ВАЖНО:
- Отвечай только на русском
- Не используй английский
- Не придумывай квартиры
- Используй только данные из списка
- Пиши кратко и понятно

История диалога:
{history}

RAG контекст:
{rag_context}

Пользователь:
{user_input}

Варианты:
{flats_text}

Объясни, почему варианты подходят.
"""

        return call_llm(prompt)