import openai

def summarize_crosstabs(prompt_text):
    system_msg = "You are an expert market research analyst. Summarize differences across demographic groups in a clear, executive-ready style."
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt_text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5
    )
    return response['choices'][0]['message']['content']
