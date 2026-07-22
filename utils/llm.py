from google import genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Models to try (in order)
MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.0-flash"
]


def generate_response(prompt):
    """
    Tries multiple Gemini models with retries.
    """

    last_error = None

    for model in MODELS:

        for attempt in range(3):   # Retry 3 times

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                last_error = e

                error = str(e)

                # Retry only if model is busy
                if "503" in error or "UNAVAILABLE" in error:
                    time.sleep(2)
                    continue

                # If model doesn't exist for this account,
                # try the next model
                if "404" in error or "NOT_FOUND" in error:
                    break

                # Quota exceeded
                if "429" in error:
                    return (
                        "❌ API quota exceeded.\n\n"
                        "Please wait for your quota to reset "
                        "or use another Gemini API key."
                    )

                # Any other unexpected error
                return f"❌ {error}"

    return (
        "❌ All Gemini models are currently unavailable.\n\n"
        "This usually happens when Google's servers are under heavy load.\n"
        "Please try again after a few minutes.\n\n"
        f"Last Error:\n{last_error}"
    )


# -------------------------------------------------
# Business Insights
# -------------------------------------------------

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


# -------------------------------------------------
# Chat with Data
# -------------------------------------------------

def ask_ai(df, question):

    prompt = f"""
You are an expert Data Analyst.

Dataset Sample:

{df.head(100).to_string()}

User Question:

{question}

Instructions:
- Answer only using the information available in the dataset.
- If the dataset doesn't contain enough information, clearly mention that.
- Keep the answer concise and well formatted.
"""

    return generate_response(prompt)



def explain_model_results(comparison_df):

    prompt = f"""
    You are a Senior Machine Learning Consultant.

    The following machine learning models were trained.

    {comparison_df.to_string(index=False)}

    Explain:

    1. Which model is best?
    2. Why is it best?
    3. Why did other models perform worse?
    4. Which model would you deploy?
    5. Keep the explanation beginner-friendly.
    """

    for model in MODELS:

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception:
            continue

    return "❌ All Gemini models are currently unavailable."
