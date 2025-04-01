import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_crosstabs(df):
    """
    Generate a GPT-powered executive summary from a cross-tabulated DataFrame.

    Assumes the first 10 rows are enough for GPT to infer the structure and differences.
    """

    try:
        # Convert the top of the table into markdown for GPT to read
        sample_text = df.head(10).to_markdown(index=False)

        prompt = f"""
You are a market research expert.

This is a cross-tabulation of survey results showing different percentages for different demographic groups.
Each row represents a question/item, and each column is a segment (e.g., Male, Female, Gen Z, Boomers, etc).

Please generate 3 to 5 key insights that highlight group differences in this format:
- [Insight]

Be specific with numbers and comparisons when possible.

Data:
{sample_text}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data insights assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        summary = response.choices[0].message.content.strip()
        return summary.splitlines()

    except Exception as e:
        return [f"❌ Error parsing file: {str(e)}"]
