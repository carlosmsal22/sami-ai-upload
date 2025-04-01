from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_crosstab(df):
    import pandas as pd
    prompt = f"""You are a market research analyst. Analyze the following cross-tabulated data and generate key insights.
    Provide comparisons, highlight notable group differences, and summarize key takeaways.

    Data:
    {df.head(30).to_markdown(index=False)}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior research analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()