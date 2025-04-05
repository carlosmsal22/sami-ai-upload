import streamlit as st
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import os
from openai import OpenAI
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="TURF Analysis", layout="wide")
st.title("📡 TURF Analysis Module")

st.markdown("Upload binary (1/0) coded data to identify optimal item combinations that maximize reach.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload CSV or Excel file with 1/0 columns", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
    st.success(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    st.dataframe(df.head())

    turf_cols = st.multiselect("Select columns to include in TURF analysis", df.columns)
    max_combo = st.slider("Maximum number of items in a combination", 2, min(10, len(turf_cols)), 3)

    if st.button("Run TURF Analysis"):
        def turf_score(combo):
            reach = (df[list(combo)].sum(axis=1) > 0).mean()
            return round(reach * 100, 2)

        all_combos = list(itertools.combinations(turf_cols, max_combo))
        results = [{"combo": c, "reach": turf_score(c)} for c in all_combos]
        results = sorted(results, key=lambda x: x["reach"], reverse=True)

        top_result = results[0]
        st.subheader("🏆 Top Combination")
        st.write(f"Items: {', '.join(top_result['combo'])}")
        st.write(f"Reach: {top_result['reach']}%")

        top_df = pd.DataFrame(results[:10])
        st.subheader("📊 Top 10 Combinations")
        st.dataframe(top_df)

        fig, ax = plt.subplots()
        ax.barh(
            [", ".join(combo["combo"]) for combo in reversed(top_df.to_dict(orient="records"))],
            list(reversed(top_df["reach"]))
        )
        ax.set_xlabel("Reach (%)")
        ax.set_title("Top TURF Combinations")
        st.pyplot(fig)

        gpt_insight = ""
        prompt = f"Here are the top TURF combinations and their reach values:\n{top_df.to_string(index=False)}"
        try:
            with st.spinner("GPT interpreting TURF results..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a TURF analysis expert."},
                        {"role": "user", "content": "Please explain the optimal strategy and implications for these TURF results."},
                        {"role": "user", "content": prompt}
                    ]
                )
                gpt_insight = response.choices[0].message.content
                st.subheader("💬 GPT Insight")
                st.markdown(gpt_insight)
        except Exception as e:
            st.error(f"GPT error: {e}")

        # PDF Report
        if gpt_insight:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="TURF Analysis Report", ln=1, align='C')
            pdf.multi_cell(0, 5, f"Top Combination:\nItems: {', '.join(top_result['combo'])}\nReach: {top_result['reach']}%")
            pdf.ln(4)
            pdf.multi_cell(0, 5, "Top 10 Combinations:")
            for _, row in top_df.iterrows():
                pdf.multi_cell(0, 5, f"{', '.join(row['combo'])}: {row['reach']}%")
            pdf.ln(4)
            pdf.multi_cell(0, 5, "GPT Insights:")
            pdf.multi_cell(0, 5, gpt_insight)

            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)

            st.download_button(
                "📥 Download PDF Report",
                data=pdf_output,
                file_name="TURF_Report.pdf",
                mime="application/pdf"
            )
