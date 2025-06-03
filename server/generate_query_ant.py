import google.generativeai as genai
import os
from typing import List


def generate_semantic_query(degree: str, courses: List[str], api_key: str) -> str:
    """
    Generate educational search query based on student's degree and courses.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Примеры желаемого формата
    example_queries = [
        "how does quicksort work algorithm explained",
        "understanding database indexing B-tree performance",
        "machine learning gradient descent explanation"
    ]

    prompt = f"""
    Student studying {degree} with courses: {', '.join(courses)}.

    Generate ONE search query for finding educational content.

    Format rules:
    - lowercase only
    - 4-8 words
    - no punctuation
    - educational focus (how things work, understanding concepts)

    Examples of good queries:
    - how does quicksort work algorithm explained
    - understanding database indexing B-tree performance
    - machine learning gradient descent explanation

    Return ONLY the query text, nothing else.
    """

    response = model.generate_content(contents=prompt)
    query = response.text.strip().lower()

    # Очистка от лишних символов
    query = ' '.join(query.split())  # Убираем лишние пробелы
    query = ''.join(c for c in query if c.isalnum() or c.isspace())  # Только буквы и пробелы

    return query


