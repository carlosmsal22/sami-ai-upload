import os
import pandas as pd
from openai import OpenAI
from tabulate import tabulate

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_summary(df: pd.DataFrame) -> str:
    preview = tabulate(df.head(30), headers='keys', tablefmt='pipe', showindex=False)
    prompt = f"""You are an expert in survey data analysis.
Below is a cross-tabulated table showing survey results by group.
Please summarize the most important differences between the groups.

{preview}

Be concise and analytical in your response."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a market research analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
