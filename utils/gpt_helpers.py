from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_comparisons(markdown_table):
    try:
        messages = [
            {"role": "system", "content": "You are a senior market researcher skilled at identifying insights from comparative data tables."},
            {"role": "user", "content": f"Analyze this segmentation data and summarize key differences:\n\n{markdown_table}"}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ GPT Error: {str(e)}"

def summarize_gpt_slide_text(text):
    try:
        messages = [
            {"role": "system", "content": "You are a senior market research strategist."},
            {"role": "user", "content": f"Summarize the following segmentation findings in a strategic executive-style summary:\n\n{text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ GPT Summary Error: {str(e)}"
