import streamlit as st
import os
import openai
from fpdf import FPDF
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import json
from io import BytesIO
import base64

# Ensure folders exist
for folder in ["avatars", "cards", "charts"]:
    os.makedirs(folder, exist_ok=True)

# Sidebar metadata
st.set_page_config(page_title="Enhanced Persona Generator", layout="wide")
st.title("🤖 Enhanced Persona Generator from PowerPoint + DALL·E Avatars")

# Upload PPTX file
pptx_file = st.file_uploader("Upload a PowerPoint (.pptx) with segmentation analysis", type=["pptx"])

def generate_avatar(description, filename):
    try:
        prompt = f"Photorealistic professional portrait of a {description}, studio lighting, neutral background."
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        image_data = openai.images.download(image_url)
        with open(os.path.join("avatars", filename), "wb") as f:
            f.write(image_data.read())
        return image_url
    except Exception as e:
        st.error(f"Failed to generate avatar: {e}")
        return None

def create_radar_chart(traits_dict, filename):
    labels = list(traits_dict.keys())
    stats = list(traits_dict.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    stats += stats[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, stats, linewidth=2, linestyle='solid')
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    plt.tight_layout()
    filepath = os.path.join("charts", filename)
    plt.savefig(filepath)
    plt.close()
    return filepath

def save_pdf(personas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('Arial', '', '', uni=True)
    pdf.set_font("Arial", size=12)

    for persona in personas:
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, txt=persona['name'], ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=persona['description'])

        avatar_path = os.path.join("avatars", persona['avatar'])
        chart_path = os.path.join("charts", persona['chart'])

        if os.path.exists(avatar_path):
            pdf.image(avatar_path, w=50)
        if os.path.exists(chart_path):
            pdf.image(chart_path, x=80, y=pdf.get_y(), w=100)

        pdf.ln(85)

    pdf_path = "personas_summary.pdf"
    pdf.output(pdf_path, "F")
    return pdf_path

# Demo personas until GPT + parsing logic is fully integrated
demo_personas = [
    {
        "name": "Simon the Solution Seeker",
        "description": "A tech-savvy urbanite who outsources cleaning and prefers modern, branded solutions.",
        "traits": {"Tech-savvy": 5, "Brand Loyal": 4, "Cleanliness-Oriented": 3, "Budget-Conscious": 2},
        "avatar": "simon_avatar.png",
        "chart": "simon_chart.png"
    },
    {
        "name": "Natalie the Neat Freak",
        "description": "A perfectionist who loves a spotless home and invests in premium cleaning tools.",
        "traits": {"Tech-savvy": 2, "Brand Loyal": 5, "Cleanliness-Oriented": 5, "Budget-Conscious": 3},
        "avatar": "natalie_avatar.png",
        "chart": "natalie_chart.png"
    }
]

if st.button("🔁 Generate Personas + Avatars"):
    for persona in demo_personas:
        st.subheader(persona["name"])
        st.markdown(persona["description"])

        avatar_url = generate_avatar(persona["description"], persona["avatar"])
        radar_path = create_radar_chart(persona["traits"], persona["chart"])

        if avatar_url:
            st.image(avatar_url, width=256)
        st.image(radar_path, caption="Trait Radar Chart")

    pdf_output = save_pdf(demo_personas)
    with open(pdf_output, "rb") as f:
        st.download_button(
            label="📄 Download Persona Summary PDF",
            data=f,
            file_name="persona_summary.pdf",
            mime="application/pdf"
        )

    st.success("All avatars, charts, and summaries exported successfully!")
    st.markdown("---")
    st.caption("POWERED BY SAMI AI INSIGHTS")
