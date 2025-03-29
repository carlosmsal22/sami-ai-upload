import openai
import os
from fpdf import FPDF
import requests
from io import BytesIO

# Load your OpenAI API key
client = openai.OpenAI(api_key="your-api-key")

# Example persona descriptions
personas = [
    {
        "name": "Simon the Solution Seeker",
        "description": "A tech-savvy urbanite who outsources cleaning and prefers modern, branded solutions."
    },
    {
        "name": "Natalie the Neat Freak",
        "description": "A perfectionist who loves a spotless home and invests in premium cleaning tools."
    },
    {
        "name": "Penny the Cost-Conscious Cleaner",
        "description": "Budget-conscious homemaker seeking value-for-money cleaning solutions."
    },
    {
        "name": "Andy the Apathetic Minimalist",
        "description": "Cares little about cleaning or brands and seeks a basic, low-cost solution."
    }
]

# Create folders for output
os.makedirs("avatars", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)

# Function to generate avatar with DALL-E 3
def generate_dalle_image(description):
    dalle_response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",  # Supported size for DALL-E 3
        quality="standard",
        n=1
    )
    return dalle_response.data[0].url

# Function to download and save image
def download_image(url, filepath):
    response = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(response.content)

# Function to generate PDF for each persona
def generate_pdf(persona_name, description, image_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Name: {persona_name}\n\nDescription: {description}")
    pdf.image(image_path, x=10, y=60, w=90)
    pdf.output(f"pdfs/{persona_name.replace(' ', '_')}.pdf")

# Main routine to generate avatars and PDFs
for persona in personas:
    name = persona["name"]
    desc = persona["description"]
    print(f"Generating for: {name}")
    try:
        avatar_url = generate_dalle_image(desc)
        avatar_path = f"avatars/{name.replace(' ', '_')}.png"
        download_image(avatar_url, avatar_path)
        generate_pdf(name, desc, avatar_path)
        print(f"Saved: {avatar_path} and PDF")
    except Exception as e:
        print(f"Error generating for {name}: {e}")
