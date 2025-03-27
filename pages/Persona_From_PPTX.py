
import streamlit as st
import os
from openai import OpenAI
from pptx import Presentation

st.set_page_config(page_title="Persona from PowerPoint", layout="wide")
st.title("📊 Persona Generator from PowerPoint (.pptx)")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload a .pptx file with audience segmentation or personas", type=["pptx"])

pptx_prompt = """
You are a persona-generating assistant. Based on this segmentation content extracted from a PowerPoint, generate 2–3 buyer personas.

Each persona should include:
- Name
- Description
- Motivations
- Frustrations
- Communication Preferences

Only use the provided content.

PowerPoint content:
{pptx_text}
"""

def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text.strip()

if uploaded_file and st.button("Generate Personas"):
    try:
        with open("temp_pptx.pptx", "wb") as f:
            f.write(uploaded_file.read())
        pptx_text = extract_text_from_pptx("temp_pptx.pptx")
        st.success("✅ Extracted text from PowerPoint.")
        with st.expander("📄 Raw Extracted Text"):
            st.text(pptx_text[:2000])  # Preview

        final_prompt = pptx_prompt.format(pptx_text=pptx_text[:4000])
        with st.spinner("Sending content to GPT..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful persona analyst."},
                    {"role": "user", "content": final_prompt}
                ]
            )
            st.subheader("🧠 Generated Personas")
            st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {e}")
