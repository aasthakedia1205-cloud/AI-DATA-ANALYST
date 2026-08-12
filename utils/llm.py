import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load local .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Cloud, use Streamlit Secrets
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)

for model in client.models.list():

    if "generateContent" in model.supported_actions:

        print(model.name)


# =========================================================
# AVAILABLE MODELS
# =========================================================

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.0-flash"
]


# =========================================================
# GENERATE RESPONSE
# =========================================================

def generate_response(prompt):

    last_error = None

    for model in MODELS:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response and response.text:
                    return response.text

            except Exception as e:

                last_error = e
                error = str(e)

                # -----------------------------
                # Server temporarily unavailable
                # -----------------------------

                if "503" in error or "UNAVAILABLE" in error:

                    if attempt < 2:
                        time.sleep(2)
                        continue

                    break

                # -----------------------------
                # Model not available
                # -----------------------------

                if "404" in error or "NOT_FOUND" in error:

                    break

                # -----------------------------
                # API quota
                # -----------------------------

                if "429" in error:

                    return (
                        "❌ Gemini API quota exceeded.\n\n"
                        "Please wait for the quota to reset "
                        "or use another Gemini API key."
                    )

                # -----------------------------
                # Authentication
                # -----------------------------

                if (
                    "401" in error
                    or "UNAUTHENTICATED" in error
                    or "authentication" in error.lower()
                ):

                    return (
                        "❌ Gemini authentication failed.\n\n"
                        "Please check the GEMINI_API_KEY "
                        "configured in Streamlit Secrets."
                    )

                # -----------------------------
                # Other error
                # -----------------------------

                return f"❌ Gemini Error:\n{error}"

    return (
        "❌ Gemini is currently unavailable.\n\n"
        "Please try again in a few moments.\n\n"
        f"Last Error:\n{last_error}"
    )


# =========================================================
# BUSINESS INSIGHTS
# =========================================================

def generate_business_insights(df):

    prompt = f"""
You are an expert Data Analyst.

Analyze the dataset below and provide:

1. Dataset Summary
2. Top 5 Business Insights
3. Data Quality Issues
4. Business Recommendations

Dataset Sample:

{df.head(100).to_string()}
"""

    return generate_response(prompt)


# =========================================================
# CHAT WITH DATA
# =========================================================

def ask_ai(df, question):

    prompt = f"""
You are an expert Data Analyst.

Dataset Sample:

{df.head(100).to_string()}

User Question:

{question}

Instructions:

- Answer only using the information available in the dataset.
- If the dataset does not contain enough information, clearly mention that.
- Do not invent information.
- Keep the answer concise and well formatted.
"""

    return generate_response(prompt)


# =========================================================
# EXPLAIN MODEL RESULTS
# =========================================================

def explain_model_results(comparison_df):

    prompt = f"""
You are a Senior Machine Learning Consultant.

The following machine learning models were trained:

{comparison_df.to_string(index=False)}

Explain:

1. Which model is best?
2. Why is it best?
3. Why did other models perform worse?
4. Which model would you deploy?
5. Keep the explanation beginner-friendly.
"""

    return generate_response(prompt)