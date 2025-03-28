import streamlit as st
from pptx import Presentation
import os
import openai
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF
import requests

st.set_page_config(page_title="Enhanced Persona From PPTX with Avatars", layout="wide")
st.title("👤 Persona Generator from PowerPoint + DALL·E Avatars")

openai.api_key = os.getenv("OPENAI_API_KEY")

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

def generate_gpt_response(prompt, role="strategist"):
    system_msg = "You are a senior market research strategist." if role == "strategist" else "You are a creative strategist who writes persona bios."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_dalle_image(description):
    try:
        dalle_response = openai.Image.create(
            prompt=description,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        return dalle_response["data"][0]["url"]
    except Exception as e:
        st.warning(f"Failed to generate image for '{description}': {e}")
        return None

# Store memory context
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = ""
if "avatars" not in st.session_state:
    st.session_state.avatars = {}

# Extract text and generate summary
if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    with st.expander("📄 Slide Text Extracted"):
        st.text(ppt_text[:2000])
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

# Generate Personas
if st.session_state.summary and st.button("👥 Generate Personas"):
    persona_prompt = f"""Based on this segmentation summary, generate 4–6 distinct personas. Each should include:
- Name
- Description
- Traits
- Pain Points
- Motivations
- Channels
- Example Messaging

Summary:
{st.session_state.summary}"""
    personas = generate_gpt_response(persona_prompt, role="persona")
    st.session_state.personas = personas
    st.subheader("🎯 Personas")
    st.markdown(personas)

# Generate Avatars
if st.session_state.personas and st.button("🖼️ Generate Persona Avatars"):
    st.subheader("🧠 Generating DALL·E Avatars...")
    st.session_state.avatars = {}
    persona_blocks = st.session_state.personas.split("Persona ")
    for block in persona_blocks[1:]:
        lines = block.strip().split("\n")
        if not lines:
            continue
        name_line = lines[0].strip()
        name = name_line.split(":")[1].strip() if ":" in name_line else name_line.strip()
        description = ""
        for line in lines:
            if "Description:" in line:
                description = line.split("Description:")[1].strip()
                break
        if name and description:
            image_url = generate_dalle_image(description)
            if image_url:
                st.session_state.avatars[name] = image_url

# Show Avatars
if st.session_state.avatars:
    st.subheader("🖼️ Persona Avatars")
    for name, url in st.session_state.avatars.items():
        st.markdown(f"**{name}**")
        st.image(url, width=300)

# Export to PDF
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + st.session_state.personas)
    buffer = BytesIO()
    pdf.output(buffer, 'F')
    buffer.seek(0)
    st.download_button("📥 Download PDF", buffer, file_name="persona_report.pdf", mime="application/pdf")
