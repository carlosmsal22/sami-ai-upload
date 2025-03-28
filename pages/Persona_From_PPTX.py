import streamlit as st
from pptx import Presentation
from io import BytesIO
import openai
from fpdf import FPDF
import textwrap

st.set_page_config(page_title="📊 Persona From PPTX", layout="wide")
st.title("📊 Persona Generator from PowerPoint")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pptx(uploaded_file):
    prs = Presentation(uploaded_file)
    full_text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text += shape.text + "\n"
    return full_text

def split_into_chunks(text, max_tokens=2000):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < max_tokens * 4:  # 1 token ≈ 4 chars (safe approx)
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_summary_from_chunks(chunks):
    summaries = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior insights analyst. Summarize the following segmentation text into bullet points including key traits, motivations, and segment definitions."},
                {"role": "user", "content": chunk}
            ]
        )
        summaries.append(response.choices[0].message.content.strip())
    return "\n\n".join(summaries)

uploaded_file = st.file_uploader("Upload a segmentation PowerPoint (.pptx)", type=["pptx"])
if uploaded_file:
    raw_text = extract_text_from_pptx(uploaded_file)
    chunks = split_into_chunks(raw_text)
    with st.spinner("Generating persona insights from slides..."):
        final_summary = generate_summary_from_chunks(chunks)

    st.subheader("📌 Executive Summary")
    st.write(final_summary)
    st.session_state["personas"] = final_summary

    # PDF Download
    if st.button("📄 Download PDF Summary"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        lines = textwrap.wrap(final_summary, 90)
        for line in lines:
            pdf.multi_cell(0, 5, line)
        buffer = BytesIO()
        pdf.output(buffer, "F")
        buffer.seek(0)
        st.download_button("📥 Download PDF", buffer, file_name="persona_summary.pdf", mime="application/pdf")
