import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from openai import OpenAI
import os
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="CBC Conjoint Analysis", layout="wide")
st.title("📦 CBC Conjoint Module")
st.caption("Estimate part-worth utilities and simulate preferences from CBC choice task data.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload CBC Choice Task Data (Excel or CSV)", type=["xlsx", "csv"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    id_col = st.selectbox("Respondent ID column", df.columns)
    task_col = st.selectbox("Task column", df.columns)
    alt_col = st.selectbox("Alternative column", df.columns)
    choice_col = st.selectbox("Choice column (1 = chosen, 0 = not chosen)", df.columns)
    attributes = st.multiselect(
        "Attributes to include in the model",
        [col for col in df.columns if col not in [id_col, task_col, alt_col, choice_col]]
    )

    if st.button("Estimate Part-Worth Utilities"):
        df_encoded = pd.get_dummies(df[attributes], drop_first=True)
        X = df_encoded
        y = df[choice_col]

        model = sm.Logit(y, X).fit(disp=False)
        utilities = model.params

        st.subheader("📊 Estimated Part-Worth Utilities")
        st.dataframe(utilities)

        fig, ax = plt.subplots(figsize=(10, 5))
        utilities.sort_values().plot(kind="barh", ax=ax)
        st.pyplot(fig)

        # GPT Insight
        prompt = f"""You are a research analyst. Based on these part-worth utilities from a CBC model:

{utilities.to_string()}

Summarize the key takeaways, attribute importance, and strategic recommendations."""
        try:
            with st.spinner("GPT analyzing..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Please summarize key findings."}
                    ]
                )
                insight = response.choices[0].message.content
                st.subheader("💬 GPT Insight")
                st.markdown(insight)

                # PDF Export
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, "CBC Conjoint Analysis", ln=1, align="C")
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 6, insight)
                pdf_output = BytesIO()
                pdf.output(pdf_output)
                pdf_output.seek(0)

                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=pdf_output,
                    file_name=f"CBC_Conjoint_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"GPT error: {e}")
