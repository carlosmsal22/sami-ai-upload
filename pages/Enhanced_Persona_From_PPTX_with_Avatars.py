import streamlit as st
import os
from openai import OpenAI
from pptx import Presentation
from fpdf import FPDF
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Enhanced Persona Generator + Avatars", layout="wide")
st.title("🎭 Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pptx(file):
    prs = Presentation(file)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

def generate_gpt_response(prompt):
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are SAMI AI, a strategic segmentation assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content.strip()

def generate_dalle_image(description, filename):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        st.image(image_url, caption=description, use_column_width=True)
        return image_url
    except Exception as e:
        st.error(f"Error generating image for {description}: {e}")
        return None

# UI
uploaded_file = st.file_uploader("📤 Upload segmentation PPTX", type=["pptx"])
if uploaded_file and st.button("📌 Generate Summary & Personas"):
    raw_text = extract_text_from_pptx(uploaded_file)
    summary_prompt = f"Extract a 5-segment summary from this content:\n{raw_text[:4000]}"
    summary = generate_gpt_response(summary_prompt)
    st.subheader("📌 Strategic Summary")
    st.markdown(summary)

    persona_prompt = f"Based on this summary, create 5 distinct personas with Name, Description, Traits, Pain Points, Motivations, Channels, Example Messaging:\n{summary}"
    personas = generate_gpt_response(persona_prompt)
    st.subheader("🎯 Personas")
    st.markdown(personas)

    # Save to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + summary)
    pdf.ln(4)
    pdf.multi_cell(0, 5, "🎯 Personas\n" + personas)
    pdf_path = "pdfs/persona_summary.pdf"
    pdf.output(pdf_path)

    with open(pdf_path, "rb") as f:
        st.download_button("📥 Download Summary PDF", f, file_name="persona_summary.pdf")

    # Optional: Avatar generation
    st.subheader("🖼️ Avatar Generation")
    lines = personas.split("Persona")
    for line in lines:
        if line.strip():
            title_line = line.split("\n")[0]
            name = title_line.strip(":").strip()
            st.markdown(f"**{name}**")
            image = generate_dalle_image(f"A realistic portrait of {name}, marketing persona, 1024x1024")