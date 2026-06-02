from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def detect_dataset_chat_intent(question, columns):
    prompt = f"""
You are a Dataset Chat Router.

Classify the user's dataset question into one intent.

Available intents:
- row_count
- column_list
- numeric_columns
- average
- minimum
- maximum
- category_count
- most_frequent
- group_total
- group_average
- top_n
- general

Dataset columns:
{columns}

Return only valid JSON like:
{{"intent":"average"}}

User question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    try:
        result = json.loads(response.choices[0].message.content)
        return result.get("intent", "general")
    except Exception:
        return "general"