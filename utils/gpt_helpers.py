
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_gpt_slide_text(df):
    prompt = f"""You are a skilled data analyst. Summarize key insights from this cross-tabulated table:
{df.head(30).to_markdown(index=False)}"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data storyteller."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error with GPT:\n{e}"

def summarize_comparisons(df):
    prompt = f"""You are an insights analyst. Compare these two groups and summarize key differences:
{df.to_markdown(index=False)}"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data storyteller."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error with GPT:\n{e}"
