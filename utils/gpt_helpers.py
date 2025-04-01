import openai
import pandas as pd
from typing import List

def summarize_crosstabs(df: pd.DataFrame) -> str:
    # Drop empty rows/columns
    df_clean = df.dropna(how='all').dropna(axis=1, how='all')

    # Extract segments from top rows
    headers = df_clean.iloc[0].fillna("").astype(str)
    data = df_clean[1:].reset_index(drop=True)

    segments = headers[3:].tolist()
    base_row = data[data.iloc[:, 2].astype(str).str.contains("BASE", na=False)]
    counts = base_row.iloc[0, 3:].tolist() if not base_row.empty else ["?" for _ in segments]

    summary = "The data provided offers a cross-tabulation of the participation rates of selected segments in market research surveys.\n\n"
    summary += "The total number of respondents for each segment (according to the 'BASE - TOTAL RESPONDENTS' row) is as follows:\n"
    for seg, count in zip(segments, counts):
        summary += f"- {seg.strip()}: {str(count).strip()}\n"

    summary += "\nHere are the insights gleaned from the data:\n"

    # Prompt for GPT
    table_str = data.head(20).to_string(index=False)
    prompt = f"""
Given the following survey cross-tabulation data, analyze the key group differences and provide 3–5 summary insights, followed by strategic recommendations.

Segments:
{segments}

Table:
{table_str}

Write a summary followed by bullet-pointed "Opportunities".
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful market research analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message["content"]

def generate_gpt_summary(df: pd.DataFrame) -> str:
    import os

    prompt = f"""
You are a research analyst. Given the following cross-tabulated table, identify the most important differences between segments.

Table:
{df.head(30).to_markdown(index=False)}

Write a comparison summary between groups, highlighting which segments differ the most and what those differences are.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful research analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message["content"]
