
import streamlit as st
import openai
import os
from pptx import Presentation
from io import BytesIO
from fpdf import FPDF

st.title("📊 Persona Generator from PowerPoint")
st.markdown("Upload a segmentation PowerPoint file and SAMI AI will extract insights and generate personas.")

openai.api_key = os.environ.get("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your PowerPoint file", type=["pptx"])

if uploaded_file:
    prs = Presentation(uploaded_file)
    full_text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text += shape.text + "\n"

    st.text_area("📄 Extracted Content", full_text, height=300)

    if st.button("🧠 Generate Persona Insights"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strategic insights consultant."},
                    {"role": "user", "content": f"Based on the following segmentation slides content, generate 3 detailed buyer personas with names, traits, motivations, pain points, preferred media channels, and messaging recommendations:\n\n{full_text}"}
                ],
                temperature=0.7
            )
            personas = response.choices[0].message.content
            st.session_state.personas = personas
            st.text_area("👤 Generated Personas", personas, height=400)

        except Exception as e:
            st.error(f"Failed to generate insights: {e}")

# PDF Export
if st.session_state.get("personas") and st.button("📄 Download Persona Report (PDF)"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    try:
        personas_text = st.session_state.personas.encode('latin-1', 'replace').decode('latin-1')
    except:
        personas_text = "Unable to encode persona text."
    pdf.multi_cell(0, 5, "👤 Personas\n\n" + personas_text)
    buffer = BytesIO()
    pdf.output(buffer, 'F')
    buffer.seek(0)
    st.download_button("📥 Download PDF", buffer, file_name="persona_report.pdf", mime="application/pdf")
