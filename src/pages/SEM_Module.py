import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from semopy import Model, Optimizer
from openai import OpenAI
import os
from fpdf import FPDF
from io import BytesIO

# App configuration
st.set_page_config(page_title="Structural Equation Modeling", layout="wide")
st.title("🧩 Structural Equation Modeling (SEM)")
st.markdown("Estimate latent and observed relationships using SEM. Upload your data and specify the model using lavaan-style syntax.")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sidebar – file upload and model input
st.sidebar.header("📅 Input Options")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
model_spec = st.sidebar.text_area("✍️ SEM Model Specification (lavaan-style)", height=200, placeholder="e.g.,\n# measurement model\nEngagement =~ Q1 + Q2 + Q3\nSatisfaction =~ Q4 + Q5\n# structural paths\nSatisfaction ~ Engagement")

# Load and preview data
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.success(f"✅ File loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
        df = None
else:
    df = None

# Run SEM
if df is not None and model_spec:
    if st.button("🚀 Run SEM Model"):
        try:
            model = Model(model_spec)
            opt = Optimizer(model)
            opt.optimize(df)

            # Display model fit
            st.subheader("📈 Model Fit Statistics")
            fit = model.inspect("gfi")
            st.dataframe(pd.DataFrame(fit.items(), columns=["Metric", "Value"]))

            # Display parameter estimates
            st.subheader("📊 Parameter Estimates")
            estimates = model.inspect()
            st.dataframe(estimates, use_container_width=True)

            # Visualize missing data distribution
            st.subheader("🧪a Missing Data Check")
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.hist(df.isnull().sum(), bins=10, color="skyblue", edgecolor="black")
            ax.set_title("Missing Data Distribution")
            ax.set_xlabel("Missing values per column")
            st.pyplot(fig)

            # GPT Summary
            with st.spinner("Generating GPT summary..."):
                prompt = f"""You are a structural equation modeling expert. Analyze the following parameter estimates:

{estimates.to_string(index=False)}

Summarize key findings, path significance, and strategic implications."""
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a SEM analyst interpreting structural equation model output."},
                        {"role": "user", "content": prompt}
                    ]
                )
                insights = response.choices[0].message.content
                st.subheader("💬 GPT Interpretation")
                st.markdown(insights)

                # Export PDF report
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 5, txt="SAMI AI - SEM Analysis Report\n\n")
                pdf.multi_cell(0, 5, insights)
                pdf_buffer = BytesIO()
                pdf.output(pdf_buffer)
                pdf_buffer.seek(0)

                st.download_button(
                    "📅 Download Summary Report (PDF)",
                    data=pdf_buffer,
                    file_name="SAMI_SEM_Report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ SEM model error: {e}")
else:
    st.info("📄 Please upload a dataset and enter a model specification to begin.")
