import google.generativeai as genai
import math
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Summarize a given text into 1–2 concise sentences using Gemini API.
def summarize_text(text: str) -> str:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Summarize the following text into 1–2 concise sentences:
    {text}
    Return only the summary.
    """
    response = model.generate_content(contents=prompt)
    return response.text.strip()


# Estimate reading time in minutes based on word count.
def estimate_reading_time(text: str) -> int:
    words = len(text.split())
    words_per_minute = 200  # Average adult reading speed
    return max(1, math.ceil(words / words_per_minute))

# Generate a concise and relevant title for a given text using Gemini API.
def generate_title(text: str) -> str:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Create a concise and relevant title for the following content:
    {text}
    Return only the title. Do not include explanations or formatting.
    """
    response = model.generate_content(contents=prompt)
    return response.text.strip()


import re

# Return the first three sentences of `text` followed by “…”.
def first_three_sentences(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    teaser = " ".join(sentences[:3])
    return teaser + ("…" if len(sentences) > 3 else "")


# Process a list of 3 texts and return an array with title, summary, and reading time.
def process_texts(text_list: list[str]) -> list[dict]:
    results = []
    for text in text_list:
        result = {
            "title": generate_title(text),
            "summary": first_three_sentences(text),
            "reading_time_minutes": estimate_reading_time(text)
        }
        results.append(result)

    return results
