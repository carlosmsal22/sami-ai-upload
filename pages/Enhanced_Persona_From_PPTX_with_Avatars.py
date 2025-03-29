
import streamlit as st
from pptx import Presentation
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)")

st.title("🤖 Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Session state setup
for key in ["summary", "personas", "avatars"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Upload PowerPoint
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

# Step 1: Segmentation Summary
if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    with st.expander("📝 Extracted Slide Text (Truncated)", expanded=False):
        st.markdown(ppt_text[:1500])

    st.info("Sending content to GPT for strategic summary...")
    summary_prompt = f"""You are SAMI AI, an advanced market insights engine. Produce a strategic summary. Include:
1. Segment Descriptions
2. Key Differentiators
3. Strategic Implications (Acquisition, Loyalty, Innovation)

Slides:
{ppt_text[:4000]}
"""
    st.session_state.summary = generate_gpt_response(summary_prompt)

if st.session_state.summary:
    st.subheader("📌 Strategic Summary")
    st.markdown(st.session_state.summary)

# Step 2: Generate Personas
if st.session_state.summary and st.button("🎯 Generate Personas"):
    persona_prompt = f"""You are SAMI AI, an insights generator. Create 5 detailed personas based on the segmentation summary. Each should include:
- Name
- Description
- Traits
- Pain Points
- Motivations
- Preferred Channels
- Example Messaging

Summary:
{st.session_state.summary}
"""
    st.session_state.personas = generate_gpt_response(persona_prompt)

if st.session_state.personas:
    st.subheader("🎯 Personas")
    st.markdown(st.session_state.personas)

# Step 3: Generate DALL·E Avatars
if st.session_state.personas and st.button("🧠 Generate Persona Avatars"):
    import re
    pattern = r"Name\s*[:：]?\s*(.*)"
    names = re.findall(pattern, st.session_state.personas)
    avatar_urls = []
    for name in names:
        desc_prompt = f"A realistic headshot portrait of {name}, professional, diverse, studio lighting"
        try:
            url = generate_dalle_image(desc_prompt)
            avatar_urls.append((name, url))
        except Exception as e:
            avatar_urls.append((name, f"❌ Error: {e}"))

    st.session_state.avatars = avatar_urls

# Display Avatars
if st.session_state.avatars:
    st.subheader("🖼️ Persona Avatars")
    for name, url in st.session_state.avatars:
        if url.startswith("http"):
            st.image(url, caption=name, use_container_width=True)
        else:
            st.warning(f"{name}: {url}")

# PDF Export
if st.session_state.personas and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + st.session_state.personas)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    st.download_button("📥 Download PDF", buffer, file_name="persona_summary.pdf", mime="application/pdf")
