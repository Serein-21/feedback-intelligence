import pandas as pd


def load_data(file_path):
    """
    Load the customer review dataset.
    """

    try:
        df = pd.read_csv(file_path)

        print("Dataset loaded successfully!")
        print(f"Total records: {len(df)}")

        return df

    except FileNotFoundError:
        print("❌ Dataset file not found.")
        return None

    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None


def clean_data(df):
    """
    Clean and prepare the dataset.
    """

    # Keep only required columns
    df = df[
        [
            "Review Title",
            "Review Text",
            "Review Date",
            "Rating",
        ]
    ].copy()

    # Rename columns
    df.rename(
        columns={
            "Review Title": "title",
            "Review Text": "review",
            "Review Date": "date",
            "Rating": "rating",
        },
        inplace=True,
    )

    # Fill missing values
    df["title"] = df["title"].fillna("")
    df["review"] = df["review"].fillna("")

    # Combine title and review
    df["title"] = df["title"].astype(str).str.strip()
    df["review"] = df["review"].astype(str).str.strip()

    df["review"] = (df["title"] + " " + df["review"]).str.strip()
    df["review"] = (
    df["review"].str.replace(r"\s+", " ", regex=True).str.strip()
    )

    # Remove empty reviews
    df = df[df["review"] != ""]

    # Remove duplicate reviews
    df.drop_duplicates(subset="review", inplace=True)

    # Remove short reviews
    df = df[df["review"].str.len() >= 20]

    # Convert review date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove invalid dates
    df.dropna(subset=["date"], inplace=True)

    # Convert rating to numeric
    df["rating"] = (
        df["rating"]
        .astype(str)
        .str.extract(r"(\d)")
        .astype(float)
    )

    # Remove invalid ratings
    df.dropna(subset=["rating"], inplace=True)

    # Sort by date
    df.sort_values("date", inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print("\n✅ Data cleaned successfully!")
    print(f"Remaining records: {len(df)}")

    return df


def preview_data(df, rows=5):
    """
    Display dataset preview and information.
    """

    print("\nFirst Few Records:")
    print(df.head(rows))

    print("\nDataset Information:")
    df.info()

    print("\nMissing Values:")
    print(df.isnull().sum())