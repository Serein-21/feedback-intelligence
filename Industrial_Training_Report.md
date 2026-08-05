SIX MONTHS INDUSTRIAL TRAINING PROJECT REPORT
ON
CUSTOMER FEEDBACK INTELLIGENCE DASHBOARD

Submitted in the Partial Fulfilment of the requirement for the Award of

Degree of [YOUR DEGREE — e.g., Bachelor of Computer Applications]

[YOUR DEPARTMENT NAME]

[UNIVERSITY NAME]

Batch [YOUR BATCH YEARS]

Submitted to: [Guide Name]
Submitted by: [Your Name], [Course & Semester], [Roll Number]

---

## ACKNOWLEDGEMENT

It is my pleasure to be indebted to various people, who directly or indirectly contributed in the development of this project and who influenced my thinking, behaviour, and acts during the course of my industrial training. I express my sincere gratitude to my project guide, **[Guide Name]**, for the valuable guidance, encouragement, and support extended throughout the duration of this training, which enabled me to understand the practical aspects of data-driven and AI-assisted software development.

I would also like to thank **[Class Incharge Name]** and the Project Incharge, **Dr. Rupinder Singh**, for their coordination and support in facilitating this industrial training as per the department's requirements.

I am grateful to my institution, **[Institution/University Name]**, for providing the platform and curriculum structure that made this training possible, and to the organisation where the training was undertaken for the practical exposure it provided.

Lastly, I would like to thank my parents for their constant moral support and my friends, with whom I shared my day-to-day experiences and received valuable suggestions that improved the quality of this work.

**[Your Name]**
**[Roll Number]**

---

## ABSTRACT

Customer reviews are one of the richest sources of feedback available to a business, yet the sheer volume of unstructured text makes manual analysis slow, inconsistent, and difficult to scale. This project, the **Customer Feedback Intelligence Dashboard**, addresses this problem by building an automated, AI-powered analytics pipeline that ingests raw Amazon customer review data, cleans and structures it, and uses a Large Language Model (LLM) to classify each review by **sentiment** (Positive, Neutral, Negative) and **topic** (Delivery, Pricing, Product Quality, Customer Service, Website/App). Classification is performed through the OpenRouter API using the `google/gemma-4-26b-a4b-it:free` model, with reviews processed in batches to reduce API overhead and a local hash-based caching mechanism to avoid re-classifying previously seen reviews. Once classified, the dataset is analysed using Pandas to compute sentiment and topic distributions, sentiment trends over time, and topic-versus-sentiment cross-tabulations. Matplotlib is used to render this analysis into a set of visual dashboards, and a final LLM call synthesises the aggregated statistics into a concise, human-readable executive summary. The result is a modular, cost-efficient, end-to-end pipeline that transforms raw customer feedback into structured insight without any manual reading of individual reviews, demonstrating practical skills in data cleaning, prompt engineering, API integration, caching strategy design, and data visualisation.

---

## INDEX

| Sr. No. | Topic | Page No. |
|---|---|---|
| | Acknowledgement | i |
| | Abstract | ii |
| 1 | Introduction | 1 |
| 1.1 | Overview | 1 |
| 1.2 | Aims and Objectives | 1 |
| 1.3 | Scope | 2 |
| 1.4 | Technologies Used | 2 |
| 2 | System Analysis | 3 |
| 2.1 | Current System vs Proposed System | 3 |
| 2.2 | Hardware and Software Requirements | 4 |
| 3 | System Design | 5 |
| 3.1 | Data / Entity Design | 5 |
| 3.2 | Data Flow Diagrams (DFD) | 6 |
| 3.3 | User Interface / Output Design | 8 |
| | Bibliography | 9 |

*(Page numbers are placeholders — Overleaf will auto-generate these once compiled with a table of contents / manual index environment.)*

---

## 1. INTRODUCTION

### 1.1 Overview

Modern e-commerce platforms generate thousands of customer reviews containing valuable but unstructured feedback. Businesses need to understand not just *how many* reviews are positive or negative, but *what specific aspects* — delivery, pricing, product quality, customer service, or the website/app experience — are driving that sentiment. Reading and categorising this volume of text manually is time-consuming, inconsistent between reviewers, and does not scale as review volume grows.

The **Customer Feedback Intelligence Dashboard** was developed during the industrial training period to solve this problem. The system automates the entire pipeline from raw review ingestion to a finished set of visual analytics and a written executive summary, using a Large Language Model as the core classification engine rather than traditional rule-based or manually trained machine learning classifiers.

### 1.2 Aims and Objectives

The project was designed with the following objectives:

1. **Automated data cleaning** — reliably transform a raw, messy CSV of customer reviews (with missing values, duplicate entries, invalid dates, and inconsistent ratings) into a clean, analysis-ready dataset.
2. **AI-based classification** — use an LLM to automatically assign a sentiment label and a topic label to every review, removing the need for manual tagging or training a custom supervised model.
3. **Cost and time efficiency** — minimise redundant API calls through batch processing and a persistent local cache, so that identical reviews are never classified twice.
4. **Insight generation** — aggregate the classified data into meaningful statistics: overall sentiment distribution, topic distribution, sentiment trends over time, and the relationship between topic and sentiment.
5. **Automated reporting** — generate a professional, statistically grounded executive summary using an LLM, without allowing the model to invent figures not present in the underlying data.

### 1.3 Scope

The system is designed to operate on structured review datasets containing, at minimum, a review title, review text, review date, and a numeric rating — the format used by Amazon product review exports. The current implementation supports:

- A fixed taxonomy of five topics (Delivery, Pricing, Product Quality, Customer Service, Website/App) and three sentiment classes (Positive, Neutral, Negative).
- Batch, offline-style processing of a static CSV file rather than real-time streaming review ingestion.
- Local output in the form of PNG chart files and a plain-text executive summary, rather than a live, interactive web dashboard.

The scope explicitly excludes real-time data ingestion, multi-language review support, and a browser-based interactive front end — these are identified as potential future enhancements.

### 1.4 Technologies Used

| Technology | Role in the Project |
|---|---|
| **Python 3.11+** | Core implementation language for the entire pipeline |
| **Pandas** | Data loading, cleaning, aggregation, and cross-tabulation |
| **Matplotlib** | Rendering bar, pie, and line charts for the dashboard |
| **OpenAI SDK (via OpenRouter)** | Interface used to call the LLM for classification and summarisation |
| **OpenRouter — `google/gemma-4-26b-a4b-it:free`** | The LLM used for sentiment/topic classification and executive summary generation |
| **python-dotenv** | Loads the `OPENROUTER_API_KEY` from a local `.env` file |
| **hashlib** | Generates MD5 hashes of review text to key the local cache |
| **json** | Serialises and deserialises cached classification results |
| **pathlib** | Cross-platform handling of project file paths |

---

## 2. SYSTEM ANALYSIS

### 2.1 Current System vs Proposed System

| Current (Manual) Approach | Proposed System (This Project) |
|---|---|
| Reviews are read manually or filtered using basic keyword search | Every review is automatically classified by sentiment and topic using an LLM |
| No structured view of trends over time | Sentiment-over-time and topic-vs-sentiment visualisations are generated automatically |
| Repeated manual effort each time new reviews arrive | A local cache (keyed by an MD5 hash of the review text) ensures previously classified reviews are never reprocessed |
| Summaries are written by hand, prone to bias or omission | An executive summary is generated by an LLM constrained strictly to the computed statistics, preventing invented figures |
| Classification consistency depends on the individual reviewer | Classification is consistent, since it is driven by a fixed prompt and taxonomy applied uniformly to every review |

### 2.2 Hardware and Software Requirements

**Software Requirements**

- Python 3.11 or higher
- Required Python packages: `pandas`, `matplotlib`, `openai`, `python-dotenv`
- An active OpenRouter account and API key, stored in a `.env` file as `OPENROUTER_API_KEY`
- A modern operating system capable of running a Python virtual environment (Windows, Linux, or macOS)

**Hardware Requirements**

- Any standard laptop or desktop computer capable of running Python (minimum 4 GB RAM recommended)
- No GPU is required, since all LLM inference is performed remotely via the OpenRouter API rather than on local hardware
- An active internet connection is mandatory, as both the classification step and the executive summary generation step depend on external API calls

---

## 3. SYSTEM DESIGN

### 3.1 Data / Entity Design

The system does not use a traditional relational database; instead, data flows through the pipeline as Pandas DataFrames and is persisted at two points: the classified CSV file and the local JSON-based cache. The logical structure of the data at each stage is as follows:

**Raw Review Record** (as loaded from `data/amazon_reviews.csv`)
- `Review Title`
- `Review Text`
- `Review Date`
- `Rating`

**Cleaned Review Record** (after `clean_data()`)
- `title` — trimmed review title
- `review` — combined and whitespace-normalised title + review text
- `date` — parsed datetime object
- `rating` — numeric rating extracted from raw text

**Classified Review Record** (after `classify_reviews_batch()`)
- All fields from the Cleaned Review Record, plus:
- `sentiment` — one of `Positive`, `Neutral`, `Negative`
- `topic` — one of `Delivery`, `Pricing`, `Product Quality`, `Customer Service`, `Website/App`

**Cache Entry** (stored under `cache/`)
- Key: MD5 hash of the review text
- Value: JSON object `{ "sentiment": ..., "topic": ... }`

This can be represented conceptually as an entity relationship where a **Review** entity is enriched through classification into two derived attributes, **Sentiment** and **Topic**, with a separate **Cache** store keyed on the review's content hash to ensure idempotent classification.

### 3.2 Data Flow Diagrams (DFD)

**Level 0 — Context Diagram**

At the highest level, the system is represented as a single process bounded by two external entities:

- **User** — provides the raw review dataset and receives the generated charts and executive summary as output.
- **OpenRouter LLM API** — receives review text (and later, aggregated statistics) and returns structured JSON classifications or generated summary text.

```
User → [Customer Feedback Intelligence Dashboard] → Charts + Executive Summary
                        ↕
                OpenRouter LLM API
```

**Level 1 — Main Processes**

The central process decomposes into six sub-processes, each corresponding directly to a module in the codebase:

| Process ID | Process Name | Module | Description |
|---|---|---|---|
| P1 | Data Loading | `loader.py — load_data()` | Reads the raw CSV file into a DataFrame; handles file-not-found and parsing errors gracefully |
| P2 | Data Cleaning | `loader.py — clean_data()` | Removes duplicates, fills missing text, filters short reviews, parses dates and ratings, sorts and resets the index |
| P3 | Batch Classification | `classifier.py — classify_reviews_batch()` | Checks the local cache for each review; sends uncached reviews to the LLM in a single batched prompt; parses and caches the JSON response, with retry logic on failure |
| P4 | Data Analysis | `analysis.py — analyze_data()` | Computes sentiment counts, topic counts, sentiment-over-time grouping, and topic-vs-sentiment cross-tabulation |
| P5 | Dashboard Generation | `dashboard.py — create_dashboard()` | Renders four Matplotlib charts (sentiment distribution, topic distribution, sentiment over time, topic vs sentiment) and saves them to the `output/` directory |
| P6 | Executive Summary Generation | `summary.py — generate_executive_summary()` | Builds a statistics-only prompt from the aggregated data and calls the LLM to produce a 140–160 word professional summary, saved as a text file |

**Data Stores**

- **D1 — Classified Reviews CSV** (`data/classified_reviews.csv`): written once by P3/`main.py` after classification, read by P4, P5, and P6.
- **D2 — Local Cache** (`cache/*.json`): read and written by P3 on every classification call, keyed by review-text hash.
- **D3 — Output Directory** (`output/`): written by P5 (chart PNGs) and P6 (`executive_summary.txt`).

**Process Flow Summary**

```
Raw CSV → P1 (Load) → P2 (Clean) → P3 (Classify, cache-aware)
        → Classified CSV (D1)
        → P4 (Analyse) → statistics
        → P5 (Dashboard) → PNG charts (D3)
        → P6 (Summary) → executive_summary.txt (D3)
```

This structure mirrors the orchestration performed by `main.py`, which calls each stage sequentially and propagates the cleaned, then classified, DataFrame through the analysis, dashboard, and summary stages.

### 3.3 User Interface / Output Design

The system is implemented as a command-line pipeline (`python main.py`) rather than a graphical application, so its "interface" is expressed through console feedback during execution and through the generated output artifacts.

**Console Output**

During execution, the pipeline prints progress and status messages at each stage, for example:

- `✅ Dataset loaded successfully!` / `❌ Dataset file not found.`
- `✅ Data cleaned successfully!` with a count of remaining records
- `Processing reviews X to Y...` for each classification batch
- `✅ Classified dataset saved to: data/classified_reviews.csv`
- `✅ Dashboard charts saved successfully!`
- `✅ Executive summary saved to: output/executive_summary.txt`

**Generated Output Artifacts**

| File | Description |
|---|---|
| `data/classified_reviews.csv` | The full cleaned dataset with added `sentiment` and `topic` columns |
| `output/sentiment_distribution.png` | Bar chart of review counts by sentiment class |
| `output/topic_distribution.png` | Pie chart of review proportions by topic |
| `output/sentiment_over_time.png` | Line chart of sentiment counts across dates |
| `output/topic_vs_sentiment.png` | Stacked bar chart cross-tabulating topic against sentiment |
| `output/executive_summary.txt` | AI-generated 140–160 word narrative summary of the dataset statistics |

This output-driven design keeps the pipeline lightweight and reproducible: any user with the required API key and a compatible CSV file can regenerate the full set of analytics and reporting artifacts with a single command.

---

## BIBLIOGRAPHY

The following resources were consulted during the design, development, and documentation of the Customer Feedback Intelligence Dashboard project.

| # | Title / Description | Source |
|---|---|---|
| 1 | Pandas Documentation | https://pandas.pydata.org/docs/ |
| 2 | Matplotlib Documentation | https://matplotlib.org/stable/contents.html |
| 3 | OpenRouter API Documentation | https://openrouter.ai/docs |
| 4 | OpenAI Python SDK Reference | https://github.com/openai/openai-python |
| 5 | python-dotenv Documentation | https://pypi.org/project/python-dotenv/ |
| 6 | Python `hashlib` Standard Library Reference | https://docs.python.org/3/library/hashlib.html |
| 7 | Python `pathlib` Standard Library Reference | https://docs.python.org/3/library/pathlib.html |
| 8 | Google Gemma Model Card | https://ai.google.dev/gemma |

*All online resources were accessed during the training period and were publicly available at the time of consultation.*
