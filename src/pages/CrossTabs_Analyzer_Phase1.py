
import streamlit as st
import pandas as pd
from io import BytesIO
import openai
import os

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

st.markdown("Upload your WinCross-style Excel file and generate banner-point comparisons with exportable insights.")

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, sheet_name="Banner", header=None)
        st.success("✅ Loaded 'Banner' sheet successfully!")
        st.dataframe(df_raw.head())

        # Clean the table: remove empty rows and reset column headers
        df_cleaned = df_raw.dropna(how='all').reset_index(drop=True)
        df_cleaned.columns = [str(c) for c in df_cleaned.iloc[0]]
        df_cleaned = df_cleaned[1:].reset_index(drop=True)

        st.subheader("🧹 Cleaned Table View")
        st.dataframe(df_cleaned)

        if st.button("🧠 Generate Executive Summary"):
            try:
                max_rows = 10
                max_cols = 6
                preview_df = df_cleaned.iloc[:max_rows, :max_cols].fillna("").astype(str)
                table_preview = preview_df.to_markdown(index=False)

                prompt = f"""
                You are a senior market research analyst. Based on the following partial cross-tab table, provide:

                - Key patterns or group differences (e.g., noticeable highs/lows)
                - Data quality issues (e.g., missing data, outliers)
                - Actionable recommendations based on the observed trends

                Here is the table preview:
                {table_preview}
                """

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a senior market research analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                insight = response.choices[0].message["content"]
                st.subheader("🧠 Executive Summary")
                st.markdown(insight)

            except Exception as e:
                st.error(f"GPT error: {e}")

        # Export cleaned table
        excel_output = BytesIO()
        df_cleaned.to_excel(excel_output, index=False)
        excel_output.seek(0)

        st.download_button("📥 Download Segment Table (Excel)", data=excel_output,
                           file_name="Cleaned_Segment_Table.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
