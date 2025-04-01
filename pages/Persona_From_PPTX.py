
import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Enhanced PPTX Persona Generator", layout="wide")
st.title("📊 Enhanced Persona Generator from PowerPoint")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior market research strategist."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Store memory context
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = ""

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
    persona_prompt = f"""Based on this segmentation summary, generate 2-3 distinct personas. Each should include:
- Name
- Description
- Traits
- Pain Points
- Motivations
- Channels
- Example Messaging

Summary:
{st.session_state.summary}"""
    personas = generate_gpt_response(persona_prompt)
    st.session_state.personas = personas
    st.subheader("🎯 Personas")
    st.markdown(personas)

# Radar Visualization
if st.session_state.personas and st.button("📈 Visualize Personas"):
    st.subheader("📊 Persona Trait Radar Chart (Mock Example)")
    labels = ['Tech-savvy', 'Budget-conscious', 'Brand loyal', 'Innovator', 'Eco-conscious']
    traits = {
        'Explorer Emma': [5, 2, 4, 5, 3],
        'Saver Sam': [2, 5, 3, 2, 4],
        'Loyal Leo': [3, 3, 5, 2, 3]
    }

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for persona, values in traits.items():
        values += values[:1]
        ax.plot(angles, values, label=persona)
        ax.fill(angles, values, alpha=0.1)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    st.pyplot(fig)

# Export to PDF
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "Personas\n" + st.session_state.personas)

    pdf_data = pdf.output(dest="S").encode("latin-1")
    st.download_button("📥 Download PDF", pdf_data, file_name="persona_report.pdf", mime="application/pdf")
