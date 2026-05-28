import json
import re
from typing import List, Dict, Any


def generate_embedding(text: str) -> List[float]:
    """
    Generate a simple embedding using TF-IDF-like hashing.
    This avoids requiring sentence_transformers and is fast for similarity comparison.
    
    Args:
        text: Input text to embed
        
    Returns:
        List of floats representing the text embedding
    """
    # Normalize and tokenize
    text_lower = text.lower()
    # Remove punctuation and split into words
    words = re.findall(r'\w+', text_lower)
    
    # Create a simple hash-based embedding (deterministic)
    embedding = []
    for i in range(384):  # Match common embedding size
        hash_val = 0
        for word in words:
            hash_val += hash(f"{word}_{i}") % 1000
        embedding.append((hash_val % 1000) / 1000.0)  # Normalize to 0-1
    
    return embedding


def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        Similarity score 0-100
    """
    if not vector1 or not vector2:
        return 0.0
        
    # Ensure vectors are same length
    min_len = min(len(vector1), len(vector2))
    v1 = vector1[:min_len]
    v2 = vector2[:min_len]
    
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(v1, v2))
    
    # Calculate magnitudes
    mag1 = sum(a * a for a in v1) ** 0.5
    mag2 = sum(b * b for b in v2) ** 0.5
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    similarity = dot_product / (mag1 * mag2)
    return round(max(0, min(1, similarity)) * 100, 2)