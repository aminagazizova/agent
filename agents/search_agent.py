import json


class SearchAgent:

    def run(self, params):

        with open("data/flats.json", "r", encoding="utf-8") as f:
            flats = json.load(f)

        results = []

        for flat in flats:

            score = 0

            if "rooms" in params:

                if flat["rooms"] == params["rooms"]:
                    score += 2

            if "max_price" in params:

                if flat["price"] <= params["max_price"]:
                    score += 1

            if "metro" in params:

                if params["metro"].lower() in flat["metro"].lower():
                    score += 2

            if score > 0:

                flat["score"] = score

                results.append(flat)

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return results