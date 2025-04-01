
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_gpt_summary(df):
    try:
        flat_df = df.dropna().astype(str).head(30).to_markdown(index=False)
        prompt = f"""You are an expert in analyzing survey data.
Given the following cross-tabulated data, identify any major insights, group differences, or trends.

Please provide:
- 3–5 bullet points summarizing key differences between segments.
- Any standout rows or statistically significant findings.
- A recommendation or interpretation if possible.

Data Table:
{flat_df}
"""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in market research analytics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating summary: {e}"

def summarize_gpt_slide_text(df):
    try:
        table_md = df.astype(str).to_markdown(index=False)
        prompt = f"""Compare and contrast the differences between these two columns of survey data.
Explain in terms of customer behavior or insights. Provide a few bullet points and be clear.

Table:
{table_md}
"""
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in behavioral insights and competitive analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ GPT Error: {e}"
