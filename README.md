# Customer Feedback Intelligence Dashboard

An AI-powered analytics dashboard that automatically analyzes customer reviews using Large Language Models (LLMs), classifies sentiment and topics, visualizes insights, and generates an executive summary.

This project was developed as part of the **Python & AI Capstone Project**.

---

## 📌 Features

- 📂 Loads and cleans customer review datasets
- 🤖 AI-based sentiment classification
  - Positive
  - Neutral
  - Negative
- 🏷️ AI-based topic classification
  - Delivery
  - Pricing
  - Product Quality
  - Customer Service
  - Website/App
- ⚡ Batch processing for efficient API usage
- 💾 Local caching to avoid repeated API calls
- 📊 Interactive visualizations using Matplotlib
- 📈 Time-series sentiment analysis
- 📝 AI-generated executive summary
- 🧩 Modular Python architecture

---

## 📁 Project Structure

```
feedback-intelligence/
│
├── cache/                     # Cached AI responses
├── data/
│   ├── amazon_reviews.csv
│   └── classified_reviews.csv
│
├── output/                    # Generated charts
│
├── src/
│   ├── loader.py
│   ├── classifier.py
│   ├── analysis.py
│   ├── dashboard.py
│   └── summary.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Technologies Used

- Python 3.11+
- Pandas
- Matplotlib
- OpenAI API (via OpenRouter)
- dotenv
- hashlib
- JSON

---

## 📊 Dataset

The project uses an Amazon customer reviews dataset containing over **1,000 customer reviews**.

Each review includes:

- Review Title
- Review Text
- Review Date
- Rating

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/customer-feedback-dashboard.git

cd customer-feedback-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_api_key_here
```

---

## ▶️ Running the Project

Run the complete pipeline:

```bash
python main.py
```

The pipeline performs the following steps:

1. Load dataset
2. Clean data
3. Classify sentiment
4. Classify topics
5. Cache responses
6. Save classified reviews
7. Generate analytics
8. Create dashboard visualizations
9. Generate executive summary

---

## 📈 Output

The project generates:

- Classified review dataset
- Sentiment distribution chart
- Topic distribution chart
- Rating distribution chart
- Sentiment trend over time
- Executive summary

---

## 🧠 Sentiment Categories

- Positive
- Neutral
- Negative

---

## 🏷️ Topic Categories

- Delivery
- Pricing
- Product Quality
- Customer Service
- Website/App

---

## 💡 Optimization

To reduce API costs and execution time, the project implements:

- Batch classification
- Response caching using hashed review text
- Duplicate request prevention

---

## 📚 Learning Outcomes

This project demonstrates:

- Data cleaning with Pandas
- Modular Python programming
- API integration
- Prompt engineering
- AI-assisted text classification
- Data visualization
- Caching strategies
- Business insight generation

---

## 📸 Sample Dashboard

Example visualizations include:

- Sentiment Distribution
- Topic Distribution
- Monthly Sentiment Trend
- Rating Distribution

---

## 📄 Future Improvements

- Streamlit web dashboard
- Interactive Plotly visualizations
- Multi-language review support
- Aspect-based sentiment analysis
- Export reports to PDF
- Real-time review monitoring

---

## 👤 Author

**Sarbjot Singh**
