import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Enhanced Persona Generator from PowerPoint + Avatars", layout="wide")
st.title("🎯 Persona Generator from PowerPoint + DALL·E Avatars")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload a PowerPoint (.pptx) with segmentation analysis", type=["pptx"])

def extract_text_from_pptx(file):
    prs = Presentation(file)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text.strip()

def generate_gpt_response(prompt):
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior market research strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content.strip()

def generate_dalle_image(description):
    dalle_response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return dalle_response.data[0].url

if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = ""
if "avatars" not in st.session_state:
    st.session_state.avatars = {}

if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    with st.expander("📄 Extracted Slide Content"):
        st.text(ppt_text[:2000])
    st.info("Sending to GPT for strategic summary...")

    summary_prompt = f"""
You are SAMI AI, a senior market strategist. Analyze the following slide content from a segmentation presentation and produce a strategic summary. Include:

1. Clear overview of all segments (segment names, attitudes, demographics)
2. Key differentiators
3. Strategic implications for:
   - Acquisition
   - Loyalty
   - Innovation

Slide Text:
{ppt_text[:4000]}
"""
    summary = generate_gpt_response(summary_prompt)
    st.session_state.summary = summary
    st.subheader("📌 Strategic Summary")
    st.markdown(summary)

if st.session_state.summary and st.button("👥 Generate Personas"):
    persona_prompt = f"""
Based on the segmentation summary, generate 5-6 unique personas. Each persona should include:

- Name
- Description
- Traits
- Pain Points
- Motivations
- Preferred Channels
- Example Messaging

Be concise, insightful, and emphasize emotional and behavioral triggers.

Segmentation Summary:
{st.session_state.summary}
"""
    personas = generate_gpt_response(persona_prompt)
    st.session_state.personas = personas
    st.subheader("🎯 Personas")
    st.markdown(personas)

if st.session_state.personas and st.button("🖼️ Generate Persona Avatars"):
    st.session_state.avatars = {}
    with st.spinner("Generating persona avatars..."):
        import re
        names = re.findall(r"Persona \d+: (.*?)\n", st.session_state.personas)
        for name in names:
            desc_match = re.search(rf"{name}\n\nDescription:\n(.*?)\n\nTraits:", st.session_state.personas, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
                prompt = f"Photorealistic professional headshot portrait of {name}, {description}. Neutral background."
                try:
                    url = generate_dalle_image(prompt)
                    st.session_state.avatars[name] = url
                except Exception as e:
                    st.warning(f"Failed to generate image for {name} : {e}")

if st.session_state.avatars:
    st.subheader("🧠 Persona Avatars")
    for name, url in st.session_state.avatars.items():
        st.image(url, caption=name, use_column_width=True)

# Export PDF
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + st.session_state.personas)
    buffer = BytesIO()
    pdf.output(buffer, "F")
    buffer.seek(0)
    st.download_button("📥 Download PDF", buffer, file_name="persona_report.pdf", mime="application/pdf")
