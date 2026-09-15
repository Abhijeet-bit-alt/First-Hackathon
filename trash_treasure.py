"""
Trash to Treasure
------------------
User enters an unwanted item; the app finds the closest matching item
in the knowledge base (using the SAME TF-IDF + cosine similarity
technique as the campus assistant) and returns reuse ideas, recycling
suggestions, DIY ideas, and an environmental tip.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TrashTreasureAssistant:
    def __init__(self, data_path="item_data.csv", similarity_threshold=0.2):
        self.data = pd.read_csv(data_path)
        self.similarity_threshold = similarity_threshold

        # Match on the "item" column instead of "question" this time --
        # same idea, different column name.
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.item_vectors = self.vectorizer.fit_transform(self.data["item"])

    def get_ideas(self, user_item):
        user_vector = self.vectorizer.transform([user_item])
        similarities = cosine_similarity(user_vector, self.item_vectors)

        best_index = similarities.argmax()
        best_score = similarities[0, best_index]

        if best_score < self.similarity_threshold:
            return None

        row = self.data.iloc[best_index]
        return {
            "matched_item": row["item"],
            "category": row["category"],
            "reuse_ideas": row["reuse_ideas"],
            "recycling_suggestions": row["recycling_suggestions"],
            "diy_ideas": row["diy_ideas"],
            "environmental_tip": row["environmental_tip"],
        }


def main():
    print("=" * 55)
    print(" Trash to Treasure (type 'exit' to quit)")
    print("=" * 55)

    assistant = TrashTreasureAssistant()

    while True:
        user_input = input("\nWhat unwanted item do you have? ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Reduce, reuse, recycle.")
            break

        if user_input == "":
            continue

        result = assistant.get_ideas(user_input)

        if result is None:
            print(
                "I don't have specific ideas for that item yet. "
                "Try something like: plastic bottle, newspaper, "
                "old t-shirt, cardboard box, glass jar, tin can, "
                "old smartphone, egg carton, wine cork, or old book."
            )
            continue

        print(f"\nClosest match: {result['matched_item']} ({result['category']})")
        print(f"Reuse idea: {result['reuse_ideas']}")
        print(f"Recycling: {result['recycling_suggestions']}")
        print(f"DIY idea: {result['diy_ideas']}")
        print(f"Did you know: {result['environmental_tip']}")


if __name__ == "__main__":
    main()
