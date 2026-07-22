from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.0-flash"
]


def generate_dashboard_recommendations(df):

    columns = df.columns.tolist()

    dtypes = df.dtypes.astype(str).to_dict()

    prompt = f"""
You are a Senior Data Analyst.

Dataset Columns:
{columns}

Column Data Types:
{dtypes}

Based on ONLY the column names and data types:

1. Identify the dataset type.
2. Give a short executive summary.
3. Suggest the top KPIs.
4. Recommend the best charts.
5. Mention any useful analysis the user should perform.

Keep the answer well formatted.
"""

    for model in MODELS:

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"{model} failed: {e}")

            continue

    return "❌ All Gemini models are currently unavailable. Please try again in a few minutes."