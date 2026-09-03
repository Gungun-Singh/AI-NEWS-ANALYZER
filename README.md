📰 AI News Analyzer

An AI-powered news article analysis tool that transforms a news article URL into a structured, easy-to-understand analysis using CAMEL AI, Groq, and Llama 3.1 8B Instant.

The application extracts the article content automatically and uses an AI agent to generate summaries, analyze sentiment, extract keywords, and identify named entities through an interactive Streamlit interface.

🚀 Live Demo

Try the application:

👉 AI News Analyzer – Live App

Replace the link above with your actual AI News Analyzer Streamlit URL.

✨ Features
📝 AI-Powered Summarization

Generate summaries at three different levels of detail:

Short: 3–5 lines
Medium: 10–15 bullet points
Detailed: 150–200 words
🌐 Multilingual Summaries

The summary can be generated in:

🇬🇧 English
🇮🇳 Hindi
Bengali
Tamil
Telugu

Only the summary is translated. Sentiment, keywords, and named entities are returned in English.

🎭 Sentiment Analysis

The AI analyzes the overall sentiment of the article:

Positive
Negative
Neutral

It also provides a short explanation for the sentiment classification.

🔑 Keyword Extraction

Automatically extracts 5–10 important keywords representing the main topics and concepts discussed in the article.

🧍 Named Entity Extraction

Identifies important entities and organizes them into:

People
Organizations
Locations
Dates
🔗 Automatic Article Extraction

Simply provide a news article URL. The application uses newspaper to download and parse the article content automatically.

🖥️ Interactive Streamlit UI

A clean dashboard allows users to:

Enter a news article URL
Select summary length
Select output language
View the article title and thumbnail
Read structured AI analysis
Access the original article
🧠 How It Works
        ┌─────────────────────┐
        │   News Article URL  │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Newspaper Parser   │
        │  Article Extraction │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │     CAMEL AI        │
        │     ChatAgent       │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │        Groq         │
        │ Llama 3.1 8B Instant│
        └──────────┬──────────┘
                   │
                   ▼
      ┌───────────────────────────┐
      │       AI Analysis         │
      │                           │
      │ 📝 Summary                │
      │ 🎭 Sentiment + Reason     │
      │ 🔑 Keywords               │
      │ 🧍 Named Entities         │
      └───────────────────────────┘
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web interface and deployment
CAMEL AI	AI agent framework
Groq	LLM inference
Llama 3.1 8B Instant	Large Language Model
newspaper	News article extraction
python-dotenv	Environment variable management
📂 Project Structure
AI-NEWS-ANALYZER/
│
├── agent.py            # CAMEL AI agent and article analysis logic
├── app.py              # Streamlit application and UI
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignored files
└── README.md           # Project documentation
📖 How to Use
Open the application.
Paste a news article URL.
Select the desired summary length.
Select the desired output language.
Click 🚀 Analyze Article.
The application extracts the article content.
The CAMEL AI agent sends the content to the Llama 3.1 model through Groq.
View the generated:
Executive Summary
Sentiment Analysis
Keywords
Named Entities
👩‍💻 Author

Gungun Singh
