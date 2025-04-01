from openai import OpenAI
import pandas as pd

client = OpenAI()  # Make sure OPENAI_API_KEY is set in your environment

def summarize_comparisons(df, question_text="the above table comparison"):
    markdown_table = df.head(30).to_markdown(index=False)

    prompt = f"""
    You are a senior market researcher.

    Analyze the following cross-tabulated data and identify:
    - Which groups differ most from others
    - What each group's behavior or preference implies
    - Any opportunities or areas of concern

    Cross-tabulated Table:
    {markdown_table}

    Provide a concise, executive-style summary in bullet points.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()
