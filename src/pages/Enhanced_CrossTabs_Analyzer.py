import streamlit as st
import pandas as pd
from io import BytesIO
import re
from openai import OpenAI
import os
from docx import Document
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("""
Upload your WinCross-style Excel file and generate deep insights + export-ready formatted tables.
""")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        sheet_df = pd.read_excel(uploaded_file, sheet_name=None, header=None)
        if "Banner" not in sheet_df:
            st.error("❌ No 'Banner' sheet found. Please upload a file with a 'Banner' sheet.")
        else:
            df = sheet_df["Banner"]
            st.success("✅ Banner sheet loaded successfully!")
            st.dataframe(df.head(10))

            # Basic parser to find table-like sections
            tables = []
            row = 0
            while row < len(df):
                if "Table Title" in str(df.iloc[row, 1]):
                    try:
                        title = str(df.iloc[row+1, 1])
                        start_row = row + 7
                        end_row = start_row + 1
                        while end_row < len(df) and isinstance(df.iloc[end_row, 2], str):
                            end_row += 3
                        table = df.iloc[start_row:end_row, 2:7].copy()
                        table.columns = ["Metric", "Group A", "Group B", "Group C", "Group D"]
                        tables.append((title, table.reset_index(drop=True)))
                        row = end_row
                    except Exception as e:
                        row += 1
                else:
                    row += 1

            if not tables:
                st.warning("⚠️ No tables parsed from Banner sheet.")
            else:
                selected = st.selectbox("Select Table to Analyze", options=range(len(tables)), format_func=lambda x: tables[x][0])
                table_title, table_df = tables[selected]
                st.subheader(f"📄 {table_title}")
                st.dataframe(table_df)

                # GPT Prompt
                preview = table_df.head(4).to_markdown(index=False)
                prompt = f"""
You are a senior market research analyst. Analyze the following cross-tab table:

Table: {table_title}

{preview}

Provide 3–5 concise but strategic insights.
Focus on what stands out, segment differences, and implications.
"""
                if st.button("🔍 Generate GPT Insights"):
                    try:
                        with st.spinner("GPT analyzing..."):
                            response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "system", "content": "You are a helpful insights analyst."},
                                    {"role": "user", "content": prompt}
                                ]
                            )
                            summary = response.choices[0].message.content
                            st.subheader("💡 GPT Insights")
                            st.markdown(summary)

                            st.session_state["last_summary"] = summary
                            st.session_state["last_table"] = table_df

                    except Exception as e:
                        st.error(f"GPT Error: {e}")

                if "last_summary" in st.session_state and st.button("📥 Export Summary Report"):
                    doc = Document()
                    doc.add_heading("SAMI AI: Executive Crosstabs Report", 0)
                    doc.add_heading(table_title, level=1)
                    doc.add_paragraph(st.session_state["last_summary"])

                    tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                    doc.save(tmp_path.name)
                    with open(tmp_path.name, "rb") as f:
                        st.download_button("Download Word Report", data=f, file_name="SAMI_Crosstabs_Report.docx")

    except Exception as e:
        st.error(f"Error reading file: {e}")
