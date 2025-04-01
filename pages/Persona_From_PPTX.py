
import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF
import re

st.set_page_config(page_title="Enhanced Persona Generator + DALL·E", layout="wide")
st.title("🧠 Persona Generator from PowerPoint with Image Avatars")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload a PowerPoint (.pptx) with segmentation content", type=["pptx"])

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
        model="gpt-3.5-turbo",
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

    return dalle_response.data[0].url

if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = ""
if "persona_images" not in st.session_state:
    st.session_state.persona_images = {}

# Step 1: Summary from PPT
if uploaded_file and st.button("🔍 Generate Strategic Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    st.info("Sending content to GPT for segmentation summary...")
    summary_prompt = f"""You are SAMI AI, an advanced insights assistant. Analyze this segmentation deck and provide a strategic summary including segment traits, differentiation, and business recommendations:

{ppt_text[:4000]}
"""
    summary = generate_gpt_response(summary_prompt)
    st.session_state.summary = summary
    st.subheader("📌 Strategic Summary")
    st.markdown(summary)

# Step 2: Persona generation
if st.session_state.summary and st.button("👥 Generate Personas"):
    persona_prompt = f"""Based on this segmentation summary, generate 2-3 distinct personas. Each should be formatted as follows:

**Name**: [Persona Name]  
**Description**: [1–2 sentence summary]  
**Traits**: [Bulleted list]  
**Pain Points**:  
**Motivations**:  
**Preferred Channels**:  
**Example Messaging**:

Summary:
{st.session_state.summary}
"""
    personas = generate_gpt_response(persona_prompt)
    st.session_state.personas = personas
    st.session_state.persona_images = {}  # reset images
    st.subheader("🎯 Personas")
    st.markdown(personas)

# Step 3: Parse and Generate DALL·E Images
if st.session_state.personas and st.button("🎨 Generate Persona Avatars"):
    persona_blocks = re.findall(r"\*\*Name\*\*: (.*?)\n\*\*Description\*\*: (.*?)\n", st.session_state.personas)
    for name, desc in persona_blocks:
        prompt = f"Professional portrait of {desc.strip()}, digital illustration, neutral background"
        try:
            img_url = generate_dalle_image(prompt)
            st.session_state.persona_images[name] = img_url
        except Exception as e:
            st.warning(f"Failed to generate image for {name}: {e}")

# Display personas + images
if st.session_state.personas:
    st.subheader("🧍 Persona Cards")
    persona_blocks = re.findall(r"\*\*Name\*\*: (.*?)\n\*\*Description\*\*: (.*?)\n", st.session_state.personas)
    for name, desc in persona_blocks:
        st.markdown(f"#### {name}")
        st.markdown(f"*{desc}*")
        if name in st.session_state.persona_images:
            st.image(st.session_state.persona_images[name], width=200)

# Step 4: Export to PDF
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "Personas\n" + st.session_state.personas)
    pdf.ln(4)
    for name, url in st.session_state.persona_images.items():
        pdf.multi_cell(0, 5, f"[Avatar Placeholder for {name}]")
    pdf_data = pdf.output(dest="S").encode("latin-1")
    st.download_button("📥 Download PDF", pdf_data, file_name="persona_report.pdf", mime="application/pdf")
