import streamlit as st
import os
from pptx import Presentation
from openai import OpenAI
from fpdf import FPDF
from io import BytesIO

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title("👤 Persona From PPTX")
st.markdown("Upload a segmentation document or paste key descriptions below.")

uploaded_file = st.file_uploader("📎 Upload PPTX", type=["pptx"])
manual_text = st.text_area("✏️ Paste your segmentation text:", height=200)

parsed_text = ""

if uploaded_file is not None:
    prs = Presentation(uploaded_file)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                parsed_text += shape.text + "\n"
elif manual_text:
    parsed_text = manual_text

if parsed_text:
    st.subheader("🔍 Extracted/Provided Text Preview")
    st.text_area("Content Preview", parsed_text, height=200)

    if st.button("🧠 Generate Persona Insights"):
        with st.spinner("Analyzing personas with GPT..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior market researcher."},
                        {"role": "user", "content": f"Given this segmentation content, extract 3 detailed buyer personas. Use headings like Name, Traits, Pain Points, Motivations, Preferred Channels, Example Messaging.\n\n{parsed_text}"}
                    ],
                    temperature=0.7
                )
                personas = response.choices[0].message.content
                st.session_state.personas = personas
                st.subheader("👥 Generated Personas")
                st.markdown(personas)
            except Exception as e:
                st.error(f"Failed to generate insights: {e}")

if "personas" in st.session_state and st.button("📄 Download PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    try:
        pdf.multi_cell(0, 5, st.session_state.personas.encode("latin-1", "replace").decode("latin-1"))
        buffer = BytesIO()
        pdf.output(buffer, 'F')
        buffer.seek(0)
        st.download_button("📥 Download PDF", buffer, file_name="persona_report.pdf", mime="application/pdf")
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
