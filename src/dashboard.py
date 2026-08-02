from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def create_dashboard():
    # Load Data
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "classified_reviews.csv"

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])

    output = project_root / "output"
    output.mkdir(exist_ok=True)

    # Sentiment Distribution
    plt.figure(figsize=(6, 4))
    df["sentiment"].value_counts().plot(kind="bar")
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Reviews")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output / "sentiment_distribution.png", dpi=300)
    plt.close()

    # Topic Distribution
    plt.figure(figsize=(7, 7))
    df["topic"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )
    plt.ylabel("")
    plt.title("Topic Distribution")
    plt.tight_layout()
    plt.savefig(output / "topic_distribution.png", dpi=300)
    plt.close()

    # Sentiment Over Time
    sentiment_time = (
        df.groupby([df["date"].dt.date, "sentiment"])
          .size()
          .unstack(fill_value=0)
    )

    sentiment_time.plot(figsize=(12, 5))
    plt.title("Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Reviews")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output / "sentiment_over_time.png", dpi=300)
    plt.close()

    # Topic vs Sentiment
    topic_sentiment = pd.crosstab(df["topic"], df["sentiment"])

    topic_sentiment.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 5)
    )

    plt.title("Topic vs Sentiment")
    plt.xlabel("Topic")
    plt.ylabel("Reviews")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output / "topic_vs_sentiment.png", dpi=300)
    plt.close()

    print("\n✅ Dashboard charts saved successfully!")


if __name__ == "__main__":
    create_dashboard()