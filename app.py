import streamlit as st
import pandas as pd
from pathlib import Path
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    layout="wide"
)

st.title("Customer Feedback Intelligence Dashboard")

# Define paths
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data" / "classified_reviews.csv"
SUMMARY_PATH = PROJECT_ROOT / "output" / "executive_summary.txt"

# Load data with caching
@st.cache_data
def load_data():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        df["date"] = pd.to_datetime(df["date"])
        return df
    return None

df = load_data()

if df is not None:
    st.sidebar.header("Dashboard Controls")
    
    # Sidebar Filters
    topics = df["topic"].unique().tolist()
    selected_topics = st.sidebar.multiselect("Filter by Topic", topics, default=topics)
    
    sentiments = df["sentiment"].unique().tolist()
    selected_sentiments = st.sidebar.multiselect("Filter by Sentiment", sentiments, default=sentiments)
    
    # Apply filters
    filtered_df = df[
        (df["topic"].isin(selected_topics)) & 
        (df["sentiment"].isin(selected_sentiments))
    ]
    
    # Executive Summary (from the LLM pipeline)
    if SUMMARY_PATH.exists():
        with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
            summary = f.read()
        st.info(f"**AI Executive Summary:**\n\n{summary}")

    # Top-level metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", len(filtered_df))
    col2.metric("Positive", len(filtered_df[filtered_df["sentiment"] == "Positive"]))
    col3.metric("Neutral", len(filtered_df[filtered_df["sentiment"] == "Neutral"]))
    col4.metric("Negative", len(filtered_df[filtered_df["sentiment"] == "Negative"]))
    
    st.markdown("---")
    
    # Charts Row 1
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("Sentiment Distribution")
        if not filtered_df.empty:
            sentiment_counts = filtered_df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            st.bar_chart(sentiment_counts.set_index("Sentiment"))
        else:
            st.write("No data for current filters.")
        
    with row1_col2:
        st.subheader("Topic Distribution")
        if not filtered_df.empty:
            topic_counts = filtered_df["topic"].value_counts().reset_index()
            topic_counts.columns = ["Topic", "Count"]
            st.bar_chart(topic_counts.set_index("Topic"))
        else:
            st.write("No data for current filters.")

    st.markdown("---")
    
    # Charts Row 2
    st.subheader("Sentiment Over Time")
    if not filtered_df.empty:
        sentiment_time = filtered_df.groupby([filtered_df["date"].dt.date, "sentiment"]).size().unstack(fill_value=0)
        st.line_chart(sentiment_time)
    else:
        st.write("No data for current filters.")

    st.markdown("---")
    
    # Data Table
    st.subheader("Review Data Explorer")
    st.dataframe(
        filtered_df[["date", "title", "review", "rating", "sentiment", "topic"]].sort_values("date", ascending=False),
        use_container_width=True
    )

else:
    st.error("Classified data not found. Please run the main pipeline (`python main.py`) first to generate the dataset.")
