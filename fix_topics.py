import pandas as pd
from pathlib import Path

csv_path = Path("data") / "classified_reviews.csv"

df = pd.read_csv(csv_path)

# Replace the invalid topic
df["topic"] = df["topic"].replace({
    "Security": "Customer Service"
})

# Save back to the same file
df.to_csv(csv_path, index=False)

print("Done! CSV permanently updated.")