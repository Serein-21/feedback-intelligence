from src.loader import load_data, clean_data, preview_data
from src.classifier import classify_reviews_batch
from src.analysis import analyze_data
from src.dashboard import create_dashboard
from src.summary import generate_executive_summary


def main():
    # -----------------------------
    # Load & Clean Data
    # -----------------------------
    file_path = "data/amazon_reviews.csv"

    df = load_data(file_path)

    if df is None:
        return

    df = clean_data(df)
    preview_data(df)

    # -----------------------------
    # AI Classification
    # -----------------------------
    batch_size = 10

    print("\nStarting batch classification...\n")

    all_results = []

    for start in range(0, len(df), batch_size):
        end = min(start + batch_size, len(df))

        print(f"Processing reviews {start + 1} to {end}...")

        reviews = df["review"].iloc[start:end].tolist()

        batch_results = classify_reviews_batch(reviews)

        all_results.extend(batch_results)

    df["sentiment"] = [result["sentiment"] for result in all_results]
    df["topic"] = [result["topic"] for result in all_results]

    # -----------------------------
    # Save Classified Dataset
    # -----------------------------
    output_file = "data/classified_reviews.csv"

    df.to_csv(output_file, index=False)

    print(f"\n✅ Classified dataset saved to: {output_file}")

    # -----------------------------
    # Analysis
    # -----------------------------
    print("\nGenerating analysis...")
    analyze_data()

    # -----------------------------
    # Dashboard
    # -----------------------------
    print("\nGenerating dashboard...")
    create_dashboard()

    # -----------------------------
    # Executive Summary
    # -----------------------------
    print("\nGenerating executive summary...")
    generate_executive_summary()

    print("\n🎉 Data generated successfully!")
    print("Check the 'output' folder for charts and the executive summary.")


if __name__ == "__main__":
    main()