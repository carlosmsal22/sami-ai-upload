
import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF
import requests

st.set_page_config(page_title="Persona Generator with Avatars", layout="wide")
st.title("🧠 Persona Generator from PowerPoint + DALL·E Avatars")

import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Upload PPTX
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
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a senior market research strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

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
if "persona_dicts" not in st.session_state:
    st.session_state.persona_dicts = []
if "avatars" not in st.session_state:
    st.session_state.avatars = {}

if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    st.info("Sending content to GPT for strategic summary...")
    summary_prompt = f"""You are SAMI AI, an advanced market insights engine. Analyze the following segmentation slides and produce a strategic summary. Include:
- Segment descriptions (demographics, attitudes)
- Key differentiators
- Strategic implications for acquisition, loyalty, and innovation

Slides:
{ppt_text[:4000]}"""
    summary = generate_gpt_response(summary_prompt)
    st.session_state.summary = summary
    st.subheader("📌 Strategic Summary")
    st.markdown(summary)

if st.session_state.summary and st.button("👥 Generate Personas"):
    persona_prompt = f"""Based on this segmentation summary, generate 5 distinct personas. Each should include:
- Name
- Description
- Traits
- Pain Points
- Motivations
- Preferred Channels
- Example Messaging

Summary:
{st.session_state.summary}"""
    personas_raw = generate_gpt_response(persona_prompt)
    st.session_state.personas = personas_raw
    st.subheader("🎯 Personas")
    st.markdown(personas_raw)

if st.session_state.personas and st.button("🖼️ Generate Persona Avatars"):
    st.session_state.avatars = {}
    st.subheader("🖼️ Persona Avatars")
    lines = st.session_state.personas.split('\n')
    current_name = ""
    for line in lines:
        if line.startswith("Persona"):
            current_name = line.split(":")[1].strip()
        elif line.startswith("Description:") and current_name:
            prompt = line.split("Description:")[1].strip()
            try:
                image_url = generate_dalle_image(prompt)
                st.session_state.avatars[current_name] = image_url
            except Exception as e:
                st.warning(f"Could not generate image for {current_name}: {e}")
            current_name = ""

    for name, url in st.session_state.avatars.items():
        st.markdown(f"**{name}**")
        if url:
            st.image(url, width=300)
            with BytesIO() as img_buf:
                img_buf.write(requests.get(url).content)
                img_buf.seek(0)
                st.download_button(f"📥 Download {name}", img_buf, file_name=f"{name}.png")
        else:
            st.warning(f"No image available for {name}.")

if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + st.session_state.personas)
    buffer = BytesIO()
    pdf.output("persona_report.pdf")
    with open("persona_report.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="persona_report.pdf", mime="application/pdf")
