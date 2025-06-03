import os
import warnings
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import time
import copy
from typing import List, Dict, Any, Tuple
from generate_query_ant import generate_semantic_query
from dotenv import load_dotenv
load_dotenv()

# Disable warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
warnings.filterwarnings('ignore')

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Global settings
BLACKLIST_WEIGHTS = {
    # Hiring keywords
    "we're hiring": 0.20,
    "we are hiring": 0.20,
    "now hiring": 0.20,
    "join our team": 0.15,
    "job opportunity": 0.15,
    "apply now": 0.20,
    "open position": 0.15,

    # Marketing/promotional
    "download link": 0.25,
    "sign up": 0.20,
    "register now": 0.20,
    "don't forget to share": 0.20,
    "spread the knowledge": 0.15,
    "#share": 0.10,
    "webinar": 0.10,
    "summit": 0.08,
    "conference": 0.08,

    # Overly promotional language
    "revolutionary": 0.10,
    "transformative power": 0.10,
    "game-changer": 0.10,
    "don't miss": 0.15,
    "limited time": 0.20
}

POSITIVE_KEYWORDS = {
    "explained": -0.10,
    "tutorial": -0.10,
    "how to": -0.08,
    "understanding": -0.08,
    "example": -0.08,
    "implementation": -0.08,
    "algorithm": -0.05,
    "code": -0.05,
    "concept": -0.05,
    "learn": -0.05,
    "tip": -0.05,
    "trick": -0.05
}


def calculate_score_adjustment(text: str) -> float:
    """Calculates score adjustment based on content"""
    text_lower = text.lower()
    total_adjustment = 0

    # Apply penalties
    for keyword, penalty in BLACKLIST_WEIGHTS.items():
        if keyword in text_lower:
            total_adjustment += penalty

    # Apply bonuses
    for keyword, bonus in POSITIVE_KEYWORDS.items():
        if keyword in text_lower:
            total_adjustment += bonus

    return total_adjustment


def adjust_score(hit: Any) -> Any:
    """Adjusts score based on content"""
    adjusted_hit = copy.deepcopy(hit)

    adjustment = calculate_score_adjustment(hit.payload['text'])

    # Apply adjustment
    adjusted_hit.score = max(0, hit.score - adjustment)

    # Save information for debugging
    adjusted_hit.payload['score_adjustment'] = adjustment
    adjusted_hit.payload['original_score'] = hit.score

    return adjusted_hit


def search_posts(degree: str, courses: List[str], limit: int = 3) -> Tuple[List[Dict[str, Any]], str]:
    """
    Main function for searching posts.

    Args:
        degree: Student degree
        courses: List of courses
        limit: Number of results to return (default 3)

    Returns:
        Tuple[List[Dict], str]: Tuple of list of posts and used query
                                 Each post contains: text, score, link, date
    """
    # Load model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Connect to Qdrant
    client = QdrantClient(host="localhost", port=6333)

    # Generate query using Gemini
    query_text = generate_semantic_query(degree, courses, GEMINI_API_KEY)

    # Encode query
    query_vector = model.encode([query_text])[0]

    # Search
    results = client.search(
        collection_name="linkedin-posts",
        query_vector=query_vector,
        limit=50  # Берем больше для лучшей фильтрации
    )

    # Apply adjustments
    adjusted_results = [adjust_score(hit) for hit in results]

    # Sort by new score
    adjusted_results.sort(key=lambda x: x.score, reverse=True)

    # Filter short posts
    filtered_results = [
        hit for hit in adjusted_results
        if len(hit.payload['text']) > 200
    ]

    # Take top results
    top_results = filtered_results[:limit]


    return [top_results[0].payload['text'],top_results[1].payload['text'],top_results[2].payload['text']]


