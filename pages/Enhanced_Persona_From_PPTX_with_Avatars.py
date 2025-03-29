import streamlit as st
from pptx import Presentation
import os
from openai import OpenAI
from io import BytesIO
from fpdf import FPDF
import requests

st.set_page_config(page_title="Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)", layout="wide")
st.title("🤖 Persona Generator from PowerPoint + DALL·E Avatars (Enhanced Debug)")

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

if "summary" not in st.session_state:
    st.session_state.summary = ""
if "personas" not in st.session_state:
    st.session_state.personas = []
if "avatar_urls" not in st.session_state:
    st.session_state.avatar_urls = {}

if uploaded_file and st.button("🔍 Generate Segmentation Summary"):
    ppt_text = extract_text_from_pptx(uploaded_file)
    st.text_area("🧾 Extracted Slide Text (Truncated)", ppt_text[:2000], height=200)
    st.info("Sending content to GPT for strategic summary...")
    prompt = f"""You are SAMI AI, an advanced market insights engine. Analyze the following segmentation slides and produce a strategic summary. Include:
- Segment descriptions (demographics, attitudes)
- Key differentiators
- Strategic implications for acquisition, loyalty, and innovation

Slides:
{ppt_text[:4000]}"""
    st.session_state.summary = generate_gpt_response(prompt)
    st.markdown("### 📌 Strategic Summary")
    st.markdown(st.session_state.summary)

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
    raw_personas = generate_gpt_response(persona_prompt)
    personas = raw_personas.split("Persona ")[1:]
    structured_personas = ["Persona " + p.strip() for p in personas if p.strip()]
    st.session_state.personas = structured_personas
    st.markdown("## 🎯 Personas")
    for p in structured_personas:
        st.markdown(p)

if st.session_state.personas and st.button("🖼 Generate Persona Avatars"):
    st.session_state.avatar_urls = {}
    for persona in st.session_state.personas:
        lines = persona.split("\n")
        name = next((line for line in lines if line.lower().startswith("name")), "Unknown")
        name_value = name.split(":", 1)[-1].strip() if ":" in name else name
        desc = next((line for line in lines if line.lower().startswith("description")), "An individual")
        try:
            url = generate_dalle_image(desc)
            st.session_state.avatar_urls[name_value] = url
        except Exception as e:
            st.warning(f"Failed to generate image for {name_value}: {e}")

if st.session_state.avatar_urls:
    st.markdown("## 🧠 Persona Avatars")
    for name, url in st.session_state.avatar_urls.items():
        st.image(url, caption=name, use_column_width=True)

# Optional download (disabled if encoding fails)
if st.session_state.personas and st.button("📥 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    try:
        pdf.multi_cell(0, 5, "📌 Strategic Summary\n" + st.session_state.summary.encode('latin1', 'replace').decode('latin1'))
        pdf.ln(4)
        for p in st.session_state.personas:
            text = p.encode('latin1', 'replace').decode('latin1')
            pdf.multi_cell(0, 5, text)
            pdf.ln(2)
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)
        st.download_button("⬇️ Download PDF", buffer, file_name="persona_debug.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
