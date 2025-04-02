import openai
import pandas as pd
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_gpt_slide_text(df):
    prompt = f"""
The following table contains survey cross-tabulation results by different customer segments. Summarize the most important differences in participation patterns, highlight the most engaged or disengaged segments, and suggest 2–3 opportunities for the client.

{df.head(30).to_markdown(index=False)}
"""
    messages = [
        {"role": "system", "content": "You are a market research analyst skilled in analyzing crosstab survey data and identifying strategic insights."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content.strip()

def compare_two_groups(df, group1, group2):
    cleaned_df = df[[group1, group2]].dropna()
    prompt = f"""
Compare these two customer segments based on their percentages in each row. Highlight significant differences and possible implications for marketing or product strategy.

{cleaned_df.to_markdown(index=False)}
"""
    messages = [
        {"role": "system", "content": "You are an expert in analyzing market research data and explaining the differences between audience segments."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(model="gpt-4", messages=messages)
    return response.choices[0].message.content.strip()