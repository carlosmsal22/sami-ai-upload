import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_gpt_slide_text(text_block: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior market research strategist."},
            {"role": "user", "content": f"Analyze this segmentation data and summarize key differences:
{text_block}"}
        ]
    )
    return response.choices[0].message.content.strip()

def summarize_comparisons(df, group_col, question_col):
    preview_text = df[[group_col, question_col]].head(30).to_string(index=False)
    return summarize_gpt_slide_text(preview_text)
