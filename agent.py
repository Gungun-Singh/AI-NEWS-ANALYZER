import os

import pdfplumber
from dotenv import load_dotenv

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.models.groq_model import GroqConfig


# ---------------------------------------------------------
# LOAD API KEY
# ---------------------------------------------------------

load_dotenv("api.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing in api.env")


# ---------------------------------------------------------
# GROQ MODEL
# ---------------------------------------------------------

model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type="openai/gpt-oss-120b",
    model_config_dict=GroqConfig(
        temperature=0.2,
        max_tokens=4096,
    ).as_dict(),
)


# ---------------------------------------------------------
# CAMEL CHAT AGENT
# ---------------------------------------------------------

agent = ChatAgent(
    system_message=(
        "You are an expert research-paper analyst. "
        "Analyze research papers accurately and never invent information."
    ),
    model=model,
)


# ---------------------------------------------------------
# EXTRACT TEXT FROM PDF
# ---------------------------------------------------------

def extract_pdf_text(pdf_path):
    """
    Extract text from all pages of a PDF.

    Returns:
        str: extracted text
        None: if extraction fails
    """

    try:
        text = ""

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            return None

        return text

    except Exception as e:

        print(f"PDF extraction failed: {e}")
        return None


# ---------------------------------------------------------
# SUMMARIZE RESEARCH PAPER
# ---------------------------------------------------------

def summarize_paper(text):
    """
    Summarize a research paper using Groq through CAMEL AI.
    """

    if not text or not isinstance(text, str) or not text.strip():

        return {
            "error": "No text was extracted from the PDF."
        }


    # -----------------------------------------------------
    # LIMIT INPUT SIZE
    # -----------------------------------------------------

    max_chars = 30000

    if len(text) > max_chars:
        text = text[:max_chars]


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
Analyze the following research paper and create a clear,
structured research digest.

Your response must contain exactly these sections:

## 1. Paper Overview
- What is the paper about?
- What problem does it address?

## 2. Research Objective
- What are the authors trying to achieve?

## 3. Methodology
- Explain the approach, model, experiment, dataset,
  framework, or methodology used.

## 4. Key Findings
- Explain the most important results and findings.

## 5. Important Concepts
- Explain important technical terms in simple language.

## 6. Limitations
- Mention limitations or weaknesses discussed in the paper.
- If the paper does not discuss limitations, say so.

## 7. Conclusion
- Explain what the research ultimately concludes.

## 8. Quick Takeaway
- Give a short 3–5 sentence explanation of what someone
  should remember after reading this paper.

IMPORTANT RULES:

- Use clear headings.
- Use bullet points where appropriate.
- Keep technical explanations understandable.
- Do not invent information.
- Only use information supported by the paper.
- If information is unavailable or unclear, explicitly say so.
- Do not include programming code unless the paper itself
  requires a tiny example for explanation.
- Do not discuss this instruction.
- Return only the research digest.

RESEARCH PAPER:

{text}
"""


    # -----------------------------------------------------
    # CALL CAMEL AGENT
    # -----------------------------------------------------

    try:

        response = agent.step(prompt)

        # CAMEL's current ChatAgent responses expose messages
        # through response.msgs / response.msg.
        if hasattr(response, "msgs") and response.msgs:

            result = response.msgs[0].content

        elif hasattr(response, "msg") and response.msg:

            result = response.msg.content

        else:

            return {
                "error": "CAMEL returned an empty response."
            }


        if not result:

            return {
                "error": "AI returned an empty summary."
            }


        return {
            "result": str(result)
        }


    except Exception as e:

        print("CAMEL/Groq error:", repr(e))

        return {
            "error": f"AI summarization failed: {str(e)}"
        }