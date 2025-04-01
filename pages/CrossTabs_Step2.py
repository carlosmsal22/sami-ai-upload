# 📄 File: utils/gpt_helpers.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_comparisons(markdown_table, context="cross-tab results"):
    prompt = f"""
You are a senior market research analyst. Analyze the following {context} and provide 3–5 key insights about differences between groups. Be concise, insightful, and specific.

{markdown_table}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior research strategist."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error with GPT: {e}"
