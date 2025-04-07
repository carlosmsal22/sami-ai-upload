# Sample Python code
print('Module loaded successfully')
import os
import openai
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_gpt_slide_text(df: pd.DataFrame) -> str:
    try:
        table_text = df.head(30).to_markdown(index=False)

        system_prompt = (
            "You are an expert market researcher. Analyze the uploaded banner table from a cross-tabulated survey file. "
            "You are expected to identify key trends, major differences between segments, and insight-rich summaries. "
            "Keep your tone executive and insight-driven."
        )

        user_prompt = f"""
Here is a sample cross-tab (banner table):

{table_text}

Please identify:
1. Key patterns or differences across segments
2. Surprising or noteworthy group behaviors
3. Strategic insights or implications

Respond with bullet points (3-5 max) suitable for an executive summary slide.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        message = response["choices"][0]["message"]["content"]
        return message

    except Exception as e:
        return f"❌ GPT error: {e}"
