import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embedding(text: str):
    return model.encode(text)


def cosine_similarity(vector1, vector2):
    similarity = np.dot(vector1, vector2) / (
            np.linalg.norm(vector1) * np.linalg.norm(vector2)
    )

    return round(float(similarity) * 100, 2)