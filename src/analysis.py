from pathlib import Path
import pandas as pd


def analyze_data():
    # Load data
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "classified_reviews.csv"

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])

    # Sentiment Counts
    sentiment_counts = df["sentiment"].value_counts()

    # Topic Counts
    topic_counts = df["topic"].value_counts()

    # Sentiment Over Time
    sentiment_over_time = (
        df.groupby([df["date"].dt.date, "sentiment"])
          .size()
          .unstack(fill_value=0)
    )

    # Topic vs Sentiment
    topic_sentiment = pd.crosstab(df["topic"], df["sentiment"])

    print("\nSentiment Counts")
    print(sentiment_counts)

    print("\nTopic Counts")
    print(topic_counts)

    print("\nSentiment Over Time")
    print(sentiment_over_time.head())

    print("\nTopic vs Sentiment")
    print(topic_sentiment)

    return (
        sentiment_counts,
        topic_counts,
        sentiment_over_time,
        topic_sentiment,
    )


if __name__ == "__main__":
    analyze_data()