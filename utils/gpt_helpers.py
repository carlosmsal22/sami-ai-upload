
def summarize_comparisons(df):
    import openai
    from tabulate import tabulate

    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        tabulated_data = tabulate(df.head(30).fillna(""), headers="keys", tablefmt="pipe", showindex=False)
        prompt = f"""
Analyze the following crosstab results. Identify the biggest differences between segments for each question. 
Summarize rows where the percentage spread between segments is high (e.g. >15%).
Present key behavioral insights and suggest implications for research strategy.

{tabulated_data}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating GPT summary: {e}"
