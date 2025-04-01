import openai
import pandas as pd

def summarize_gpt_slide_text(df):
    content = df.head(30).to_markdown(index=False)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"Analyze this segmentation data and summarize key differences:

{content}"}
        ]
    )
    return response.choices[0].message.content.strip()

def summarize_comparisons(df, col1, col2):
    try:
        comp_df = df[[col1, col2]].dropna()
        content = comp_df.to_markdown(index=False)
    except Exception as e:
        raise ValueError(f"Formatting issue when extracting comparison columns: {e}")

    prompt = f"""Compare the following two segments based on their responses. Identify key statistical or perceptual differences.

Group 1: {col1}
Group 2: {col2}

Data:
{content}
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
