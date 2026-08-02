import hashlib
import json
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

CACHE_DIR = "cache"

TOPICS = [
    "Delivery",
    "Pricing",
    "Product Quality",
    "Customer Service",
    "Website/App",
]


def get_cache_path(review: str) -> str:
    """Return cache file path for a review."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    review_hash = hashlib.md5(review.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{review_hash}.json")


def load_cache(review: str):
    """Load cached classification if available."""
    cache_path = get_cache_path(review)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as file:
            return json.load(file)

    return None


def save_cache(review: str, result: dict):
    """Save classification to cache."""
    with open(get_cache_path(review), "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def classify_review(review: str) -> dict:
    """
    Classify a single customer review.
    """

    cached = load_cache(review)
    if cached is not None:
        return cached

    topics = "\n".join(f"- {topic}" for topic in TOPICS)

    prompt = f"""
You are a customer feedback analyst.

Analyze the following review.

Review:
{review}

Classify it into:

1. Sentiment:
- Positive
- Neutral
- Negative

2. Topic (choose exactly one):
{topics}

Return ONLY a valid JSON object.

{{
    "sentiment": "Positive",
    "topic": "Delivery"
}}
"""

    try:
        response = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        result = json.loads(content)

        save_cache(review, result)

        return result

    except Exception as e:
        print(f"Classification Error: {e}")

        return {
            "sentiment": "Unknown",
            "topic": "Unknown",
        }


def classify_reviews_batch(reviews: list) -> list:
    """
    Classify multiple reviews in one API call.
    """

    results = []
    reviews_to_classify = []
    review_indices = []

    # Check cache
    for i, review in enumerate(reviews):
        cached = load_cache(review)

        if cached is not None:
            results.append(cached)
        else:
            results.append(None)
            reviews_to_classify.append(review)
            review_indices.append(i)

    if not reviews_to_classify:
        return results

    topics = "\n".join(f"- {topic}" for topic in TOPICS)

    review_list = "\n\n".join(
        f"Review {i + 1}:\n{review}"
        for i, review in enumerate(reviews_to_classify)
    )

    prompt = f"""
You are a customer feedback analyst.

Analyze each customer review below.

For EACH review classify:

1. Sentiment:
- Positive
- Neutral
- Negative

2. Topic (choose exactly one):
{topics}

Reviews:
{review_list}

Return ONLY a valid JSON array.

Example:

[
    {{
        "sentiment": "Positive",
        "topic": "Delivery"
    }},
    {{
        "sentiment": "Negative",
        "topic": "Customer Service"
    }}
]

Do not include markdown.
Do not include explanations.
Do not include code fences.
"""

    for attempt in range(3):

        try:
            response = client.chat.completions.create(
                model="google/gemma-4-26b-a4b-it:free",
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = response.choices[0].message.content.strip()

            if content.startswith("```"):
                content = (
                    content.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            batch_results = json.loads(content)

            for index, result in zip(review_indices, batch_results):
                results[index] = result
                save_cache(reviews[index], result)

            return results

        except Exception as e:

            print(f"Attempt {attempt + 1}/3 failed: {e}")

            if attempt < 2:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Skipping this batch.")

                return [
                    {
                        "sentiment": "Unknown",
                        "topic": "Unknown",
                    }
                    for _ in reviews
                ]