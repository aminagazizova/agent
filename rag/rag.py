from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = []
embeddings = []

RAG_FOLDER = "rag"

for file in os.listdir(RAG_FOLDER):
    if file.endswith(".md"):
        with open(os.path.join(RAG_FOLDER, file), encoding="utf-8") as f:
            text = f.read()

            chunks = text.split("\n")

            for chunk in chunks:
                if chunk.strip():
                    documents.append(chunk)

embeddings = model.encode(documents)

def retrieve(query, top_k=3):
    query_embedding = model.encode([query])[0]

    scores = np.dot(embeddings, query_embedding)

    top_indices = np.argsort(scores)[-top_k:][::-1]

    return [documents[i] for i in top_indices]