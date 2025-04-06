import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from openai import OpenAI
import os

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

st.markdown("""
Upload your WinCross-style Excel file and generate banner-point comparisons with exportable insights.
""")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if uploaded_file:
    try:
        all_sheets = pd.read_excel(uploaded_file, sheet_name=None, header=None)
        if "Banner" in all_sheets:
            df_raw = all_sheets["Banner"]
            st.success("✅ Loaded 'Banner' sheet successfully!")

            # Display a preview
            st.dataframe(df_raw.head())

            # Extract and clean the top-most table
            clean_table = df_raw.iloc[10:].copy()
            clean_table.columns = df_raw.iloc[9]
            clean_table = clean_table.reset_index(drop=True)
            st.markdown("### 🔍 Cleaned Table View")
            st.dataframe(clean_table.head())

            # GPT Executive Summary
            if st.button("🧠 Generate Executive Summary"):
                table_str = clean_table.to_string(index=False)
                prompt = f"""
You are a senior market research analyst. Provide a strategic executive summary of the following banner-point cross-tab table.

Identify:
- Patterns or group differences
- Any missing data or anomalies
- Actionable implications

Here is the table:
{table_str}
                """

                try:
                    with st.spinner("Analyzing with GPT..."):
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a strategic analyst specializing in cross-tab research."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        st.subheader("🧠 Executive Summary")
                        st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"GPT error: {e}")

            # Download button
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                clean_table.to_excel(writer, index=False, sheet_name="Segment Table")
            output.seek(0)
            st.download_button("📥 Download Segment Table (Excel)", data=output, file_name="segment_table.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        else:
            st.error("❌ 'Banner' sheet not found in Excel file.")
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
