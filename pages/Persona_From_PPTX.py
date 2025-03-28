import streamlit as st
import openai
from io import BytesIO
from fpdf import FPDF
import requests
from PIL import Image
import base64

st.set_page_config(page_title="Persona Generator + Avatars", layout="wide")

st.title("👤 Persona Generator with AI Avatars")
st.markdown("Upload a segmentation document or paste key descriptions below.")

# Load OpenAI API key
import os
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ---- TEXT INPUT ----
prompt_input = st.text_area("Paste your segmentation text:", height=300)

if st.button("Generate Personas & Avatars") and prompt_input:
    with st.spinner("Generating personas using GPT-4..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert market researcher."},
                    {"role": "user", "content": f"From the following segmentation summary, generate 3 unique personas including: name, description, 3-5 traits, pain points, motivations, preferred channels, and suggested marketing message.\n\nText: {prompt_input}"}
                ]
            )
            output = response["choices"][0]["message"]["content"]
            st.session_state.personas_text = output
        except Exception as e:
            st.error(f"GPT Error: {e}")

    # Parse into personas
    if "personas_text" in st.session_state:
        personas = []
        current = {}
        for line in st.session_state.personas_text.split("\n"):
            line = line.strip()
            if line.startswith("Name:"):
                if current: personas.append(current)
                current = {"name": line.split(":",1)[1].strip()}
            elif line.startswith("Description:"):
                current["desc"] = line.split(":",1)[1].strip()
        if current: personas.append(current)

        cols = st.columns(len(personas))

        for i, p in enumerate(personas):
            with cols[i]:
                st.markdown(f"**{p['name']}**")
                st.caption(p['desc'])

                try:
                    dalle_response = openai.Image.create(
                        model="dall-e-3",
                        prompt=f"Portrait photo of {p['desc']}, realistic, centered, professional",
                        size="1024x1024",
                        n=1
                    )
                    image_url = dalle_response.data[0].url
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    st.image(image, caption=f"{p['name']}", use_column_width=True)

                    # Download button
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    b64_img = base64.b64encode(buffered.getvalue()).decode()
                    st.download_button(
                        label="📥 Download Avatar",
                        data=buffered,
                        file_name=f"{p['name'].replace(' ','_')}.png",
                        mime="image/png"
                    )

                except Exception as e:
                    st.warning("⚠️ Avatar generation failed")
                    st.image("https://via.placeholder.com/300x300.png?text=No+Image", caption="Placeholder")

# ---- Download Personas as PDF ----
if "personas_text" in st.session_state and st.button("📄 Download Full PDF Summary"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    safe_text = st.session_state.personas_text.encode("latin-1", errors="ignore").decode("latin-1")
    pdf.multi_cell(0, 5, safe_text)
    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    st.download_button("📥 Download PDF", buf, file_name="personas_summary.pdf", mime="application/pdf")
