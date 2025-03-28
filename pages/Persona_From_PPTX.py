import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
from fpdf import FPDF
import re

st.set_page_config(page_title="🧠 Persona Generator with Avatars", layout="wide")
st.title("🧠 Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)")

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
    response = client.chat.completions.create(
        model="gpt-4",
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

# SESSION STATE INIT
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = ""
if "avatar_urls" not in st.session_state:
    st.session_state.avatar_urls = {}

# STEP 1: Generate Strategic Summary
if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    with st.expander("📄 Slide Text Extracted"):
        st.text(ppt_text[:3000])
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

# STEP 2: Generate Personas with Avatar Image Prompts
if st.session_state.summary and st.button("👥 Generate Personas"):
    summary_text = st.session_state.summary
    match = re.search(r'(\d+)\s+segments?', summary_text.lower())
    num_segments = int(match.group(1)) if match else 5

    persona_prompt = f"""You are SAMI AI, an advanced segmentation strategist.

Based on the segmentation summary below, generate exactly {num_segments} distinct personas.

Each persona must include:
## Name
## Description
## Traits
## Pain Points
## Motivations
## Preferred Channels
## Example Messaging

Summary:
{summary_text}"""
    personas = generate_gpt_response(persona_prompt)
    st.session_state.personas = personas
    st.subheader("🎯 Personas")
    st.markdown(personas)

    st.session_state.avatar_urls = {}
    persona_blocks = personas.split("## Name")[1:]
    if not persona_blocks:
        st.warning("⚠️ No persona blocks found. Please check the formatting of the GPT output.")
    for block in persona_blocks:
        name_line = block.strip().split("\n")[0]
        description = ""
        if "## Description" in block:
            try:
                description = block.split("## Description")[1].split("\n")[0].strip()
            except:
                continue
        if description:
            try:
                st.markdown(f"🧪 Generating image for: {name_line}")
                st.markdown(f"📝 Prompt: {description}")
                image_url = generate_dalle_image(description)
                st.session_state.avatar_urls[name_line] = image_url
            except Exception as e:
                st.warning(f"⚠️ Failed to generate image for {name_line}: {e}")

# STEP 3: SHOW AVATARS
if st.session_state.avatar_urls:
    st.subheader("🖼️ Persona Avatars")
    for name, url in st.session_state.avatar_urls.items():
        st.image(url, caption=name)

# STEP 4: PDF Download
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + st.session_state.personas)
    buffer = BytesIO()
    pdf.output("persona_debug.pdf")
    with open("persona_debug.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="persona_report.pdf", mime="application/pdf")
