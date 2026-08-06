import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# ── Plotly template that follows Streamlit's theme ────────────────────────────
pio.templates.default = "plotly_dark"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Feedback Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Minimal custom CSS ────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Remove default top padding */
        .block-container { padding-top: 2rem; }

        /* Metric cards -- works in both light and dark */
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 8px;
            padding: 1rem 1.2rem;
        }

        /* Section headers */
        h2 { font-size: 1.1rem !important; font-weight: 600; margin-bottom: 0.5rem; }

        /* Hide Streamlit branding */
        #MainMenu, footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data loading ──────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).parent / "data" / "classified_reviews.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    return df

# ── Guard: file must exist ────────────────────────────────────────────────────
if not DATA_PATH.exists():
    st.error("classified_reviews.csv not found in data/. Run main.py first.")
    st.stop()

df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Filters")

    sentiment_opts = sorted(df_full["sentiment"].dropna().unique().tolist())
    selected_sentiments = st.multiselect(
        "Sentiment", sentiment_opts, default=sentiment_opts
    )

    topic_opts = sorted(df_full["topic"].dropna().unique().tolist())
    selected_topics = st.multiselect("Topic", topic_opts, default=topic_opts)

    min_date = df_full["date"].min().date()
    max_date = df_full["date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date))

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_full.copy()

if selected_sentiments:
    df = df[df["sentiment"].isin(selected_sentiments)]

if selected_topics:
    df = df[df["topic"].isin(selected_topics)]

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Customer Feedback Intelligence")
st.caption("AI-classified Amazon review analytics")
st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
total = len(df)
positive_pct = round(len(df[df["sentiment"] == "Positive"]) / total * 100, 1) if total else 0
negative_pct = round(len(df[df["sentiment"] == "Negative"]) / total * 100, 1) if total else 0
avg_rating   = round(df["rating"].mean(), 2) if total else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reviews", f"{total:,}")
col2.metric("Positive", f"{positive_pct}%")
col3.metric("Negative", f"{negative_pct}%")
col4.metric("Avg Rating", f"{avg_rating} / 5")

st.divider()

# ── Row 1: Sentiment + Topic distribution ────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Sentiment Distribution")
    sent_counts = df["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Count"]
    color_map = {"Positive": "#2a9d8f", "Neutral": "#e9c46a", "Negative": "#ef6f51"}
    fig_sent = px.bar(
        sent_counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        color_discrete_map=color_map,
        text="Count",
    )
    fig_sent.update_traces(textposition="outside")
    fig_sent.update_layout(
        showlegend=False,
        margin=dict(t=30, b=20, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        xaxis=dict(showgrid=False),
        font=dict(family="sans-serif", size=13),
    )
    st.plotly_chart(fig_sent, use_container_width=True)

with col_right:
    st.subheader("Topic Distribution")
    topic_counts = df["topic"].value_counts().reset_index()
    topic_counts.columns = ["Topic", "Count"]
    fig_topic = px.bar(
        topic_counts,
        x="Count",
        y="Topic",
        orientation="h",
        text="Count",
        color_discrete_sequence=["#4ea8de"],
    )
    fig_topic.update_traces(textposition="outside")
    fig_topic.update_layout(
        showlegend=False,
        margin=dict(t=30, b=20, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(showgrid=False),
        font=dict(family="sans-serif", size=13),
    )
    st.plotly_chart(fig_topic, use_container_width=True)

# ── Row 2: Sentiment over time + Rating distribution ─────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Sentiment Trend Over Time")
    trend = (
        df.groupby([df["date"].dt.to_period("M"), "sentiment"])
        .size()
        .reset_index(name="Count")
    )
    trend["date"] = trend["date"].dt.to_timestamp()
    fig_trend = px.line(
        trend,
        x="date",
        y="Count",
        color="sentiment",
        color_discrete_map=color_map,
        markers=True,
    )
    fig_trend.update_layout(
        margin=dict(t=20, b=20, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        xaxis_title="Month",
        yaxis_title="Reviews",
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        xaxis=dict(showgrid=False),
        font=dict(family="sans-serif", size=13),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right2:
    st.subheader("Rating Distribution")
    rating_counts = df["rating"].value_counts().sort_index().reset_index()
    rating_counts.columns = ["Rating", "Count"]
    rating_counts["Rating"] = rating_counts["Rating"].astype(str)
    fig_rating = px.bar(
        rating_counts,
        x="Rating",
        y="Count",
        text="Count",
        color_discrete_sequence=["#48bfe3"],
    )
    fig_rating.update_traces(textposition="outside")
    fig_rating.update_layout(
        showlegend=False,
        margin=dict(t=30, b=20, l=0, r=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Star Rating",
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        xaxis=dict(showgrid=False),
        font=dict(family="sans-serif", size=13),
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# ── Row 3: Topic x Sentiment heatmap ─────────────────────────────────────────
st.subheader("Topic vs Sentiment Breakdown")

topic_sent = pd.crosstab(df["topic"], df["sentiment"])

# Ensure column order
for col in ["Positive", "Neutral", "Negative"]:
    if col not in topic_sent.columns:
        topic_sent[col] = 0
topic_sent = topic_sent[["Positive", "Neutral", "Negative"]]

fig_heat = px.imshow(
    topic_sent,
    text_auto=True,
    color_continuous_scale="Blues",
    aspect="auto",
)
fig_heat.update_layout(
    margin=dict(t=10, b=10, l=0, r=0),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    font=dict(family="sans-serif", size=13),
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Executive Summary ─────────────────────────────────────────────────────────
st.divider()
st.subheader("Executive Summary")

summary_path = Path(__file__).parent / "output" / "executive_summary.txt"
if summary_path.exists():
    st.markdown(summary_path.read_text(encoding="utf-8"))
else:
    st.markdown(
        "This capstone project presents a comprehensive sentiment analysis of a "
        "large-scale consumer feedback dataset comprising 1,198 total reviews. The "
        "findings reveal a significant trend in user dissatisfaction, as negative "
        "sentiment accounts for 86.5% of the total feedback. In contrast, positive "
        "sentiment represents only 11.4% of the data, while neutral expressions "
        "constitute a minimal 2.1%.\n\n"
        "A detailed thematic breakdown highlights the primary drivers of customer "
        "sentiment. Customer Service emerges as the most prominent area of concern, "
        "accounting for 502 instances, closely followed by Delivery issues with 424 "
        "instances. Other significant areas of focus include Product Quality, which "
        "was identified 117 times, alongside concerns regarding the Website/App and "
        "Pricing. Security concerns were negligible, representing a single instance. "
        "These results indicate that improving service interactions and logistics "
        "efficiency is critical for addressing the overwhelming majority of negative "
        "user experiences within the current operational framework."
    )

# ── Row 4: Raw data table ─────────────────────────────────────────────────────
st.divider()
with st.expander("View raw data"):
    display_df = df[["date", "rating", "sentiment", "topic", "review"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    display_df.columns = ["Date", "Rating", "Sentiment", "Topic", "Review"]
    st.dataframe(display_df, use_container_width=True, height=320)
    st.caption(f"{len(display_df):,} rows shown")
