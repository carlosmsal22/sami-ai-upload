from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_gpt_slide_text(slide_text):
    prompt = f"""You are a seasoned market research strategist. Analyze the following segmentation banner tables and summarize key differences across demographic groups. Focus on:
- Where one group significantly differs from others
- Use %s to quantify insights
- Keep it concise and actionable

Here’s the data:
{slide_text}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an insights analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
