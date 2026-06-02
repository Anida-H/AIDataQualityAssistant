from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def detect_intent(question):
    prompt = f"""
You are an AI Data Quality Agent.

Your job is to classify the user's question into ONE intent.

Available intents:

- missing_values
- duplicates
- outliers
- quality_score
- recommendations
- summary
- explain
- next_step
- ml_readiness
- preprocessing
- problematic_columns
- general

Return ONLY valid JSON.

Example:

{{"intent":"missing_values"}}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
        return result["intent"]
    except:
        return "general"