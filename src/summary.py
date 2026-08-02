from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


def generate_executive_summary():
    # Load API Key
    load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    # Load Data
    project_root = Path(__file__).resolve().parent.parent
    df = pd.read_csv(project_root / "data" / "classified_reviews.csv")

    # Aggregate Statistics
    total_reviews = len(df)

    sentiments = df["sentiment"].value_counts()
    topics = df["topic"].value_counts()

    negative = sentiments.get("Negative", 0)
    positive = sentiments.get("Positive", 0)
    neutral = sentiments.get("Neutral", 0)

    stats = f"""
Dataset Statistics

Total Reviews: {total_reviews}

Sentiment Distribution:
- Negative: {negative} ({negative / total_reviews * 100:.1f}%)
- Positive: {positive} ({positive / total_reviews * 100:.1f}%)
- Neutral: {neutral} ({neutral / total_reviews * 100:.1f}%)

Topic Distribution:
{topics.to_string()}
"""

    prompt = f"""
You are writing the executive summary section for a university capstone project.

Use ONLY the aggregated statistics below.
Do NOT mention raw reviews.
Do NOT invent numbers.
Write between 140 to 160 words.
Use a professional but natural tone.

Statistics:
{stats}
"""

    response = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    summary = response.choices[0].message.content

    output_path = project_root / "output"
    output_path.mkdir(exist_ok=True)

    output_file = output_path / "executive_summary.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)

    print(summary)
    print(f"\n✅ Executive summary saved to: {output_file}")


if __name__ == "__main__":
    generate_executive_summary()