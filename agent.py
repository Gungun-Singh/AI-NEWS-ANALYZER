# agent.py
import os
from dotenv import load_dotenv

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.configs import GroqConfig
from camel.agents import ChatAgent

# Load API keys
load_dotenv("api.env")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY missing in api.env")

# ----------- MODEL SETUP -----------
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type="llama-3.1-8b-instant",
    model_config_dict=GroqConfig(temperature=0.2).as_dict(),
)

# ----------- AGENT SETUP -----------
summary_agent = ChatAgent(
    system_message=(
        "You are an expert AI news analyst. "
        "You will do structured multi-point summarization, sentiment analysis, "
        "keyword extraction, entity extraction, and multilingual output."
    ),
    model=model
)

# ----------- ADVANCED SUMMARIZER FUNCTION -----------
def analyze_article(text: str, summary_length: str = "Medium", language: str = "English") -> dict:
    """
    Returns summary, sentiment, keywords, and entities.
    summary_length = Short (3–5 lines), Medium (10–15 points), Detailed (150–200 words)
    language = English, Hindi, Bengali, Tamil, Telugu
    """

    if not text or len(text.strip()) == 0:
        return {"error": "No content available for summarization."}

    prompt = f"""
    You are an AI news analysis assistant.

    Perform the following tasks for the given article:

    1. **SUMMARY**
       - If summary_length="Short": Summarize in 3–5 lines.
       - If summary_length="Medium": Give 10–15 bullet points.
       - If summary_length="Detailed": Write a detailed 150–200 word summary.

    2. **SENTIMENT**
       - Provide overall sentiment: Positive / Negative / Neutral.
       - Give a 1–2 line justification.

    3. **KEYWORDS**
       - Extract 5–10 important keywords.

    4. **ENTITIES**
       - Extract named entities under: People, Organizations, Locations, Dates.

    5. **LANGUAGE OUTPUT**
       - Translate ONLY the summary to the requested language: {language}
       - Sentiment, keywords, and entities remain in English.

    Format your response EXACTLY as follows:

    SUMMARY:
    <translated summary>

    SENTIMENT:
    <sentiment>

    REASON:
    <explanation>

    KEYWORDS:
    - keyword1
    - keyword2

    ENTITIES:
    PEOPLE: ...
    ORGANIZATIONS: ...
    LOCATIONS: ...
    DATES: ...

    Article:
    {text}
    """

    response = summary_agent.step(prompt)
    return {"result": response.msgs[0].content}
