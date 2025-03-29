
import streamlit as st
import os
from PIL import Image
import matplotlib.pyplot as plt
from fpdf import FPDF

# === Directory Setup ===
AVATAR_DIR = "avatars"
CARD_DIR = "cards"
CHART_DIR = "charts"
PDF_DIR = "pdfs"

for folder in [AVATAR_DIR, CARD_DIR, CHART_DIR, PDF_DIR]:
    os.makedirs(folder, exist_ok=True)

# === Style Selector ===
avatar_style = st.selectbox(
    "Choose Avatar Style",
    ["photo-realistic", "mid-century modern", "cartoon", "flat illustration"]
)

# === Sample Persona Data (for demo) ===
personas = [
    {"name": "Simon the Solution Seeker", "description": "tech-savvy urbanite who outsources cleaning and prefers modern, branded solutions."},
    {"name": "Natalie the Neat Freak", "description": "perfectionist who loves a spotless home and invests in premium cleaning tools."}
]

# === Simulated Avatar + Radar Chart Generation ===
for persona in personas:
    name = persona["name"].replace(" ", "_")
    
    # === Avatar Simulation ===
    avatar_img = Image.new("RGB", (300, 300), color=(180, 200, 255))
    avatar_path = os.path.join(AVATAR_DIR, f"{name}_avatar.png")
    avatar_img.save(avatar_path)
    st.image(avatar_path, caption=f"{persona['name']}", use_column_width=True)
    
    # === Radar Chart Simulation ===
    traits = ["Tech-savvy", "Cleanliness", "Brand Loyal", "Budget-Conscious"]
    scores = [4, 3, 5, 2] if "Simon" in name else [2, 5, 4, 3]
    angles = [n / float(len(traits)) * 2 * 3.14159 for n in range(len(traits))]
    scores += scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, scores, linewidth=2)
    ax.fill(angles, scores, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits)
    
    chart_path = os.path.join(CHART_DIR, f"{name}_radar.png")
    plt.savefig(chart_path, bbox_inches='tight')
    st.image(chart_path, caption="Trait Radar Chart")
    plt.close()

    # === Persona Card Composition ===
    avatar = Image.open(avatar_path)
    chart = Image.open(chart_path)
    card = Image.new("RGB", (avatar.width, avatar.height + chart.height))
    card.paste(avatar, (0, 0))
    card.paste(chart, (0, avatar.height))
    
    card_path = os.path.join(CARD_DIR, f"{name}_card.png")
    card.save(card_path)

# === PDF Summary Generation ===
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Persona Summary", ln=True, align="C")

pdf = PDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)
for persona in personas:
    pdf.multi_cell(0, 10, f"{persona['name']}\n{persona['description']}\n\n")

pdf_path = os.path.join(PDF_DIR, "persona_summary.pdf")
pdf.output(pdf_path)
st.success("All outputs saved successfully!")
