
import streamlit as st
import pandas as pd
from io import BytesIO
import re
import openpyxl
from openai import OpenAI
import os

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

st.markdown("Upload your WinCross-style Excel file and generate deep insights + export-ready formatted tables.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Banner", header=None)
        st.success("✅ Loaded 'Banner' sheet successfully")

        def parse_wincross_tables(df):
            tables = []
            row = 0
            while row < len(df):
                if "Table Title" in str(df.iloc[row, 1]):
                    title = str(df.iloc[row + 1, 1])
                    base_counts = df.iloc[row + 6, 3:7].tolist()
                    segments = [f"Segment {i+1} (n={int(v)})" if pd.notnull(v) else f"Segment {i+1}" for i, v in enumerate(base_counts)]
                    rows = []
                    sub_row = row + 8
                    while sub_row + 2 < len(df) and isinstance(df.iloc[sub_row, 2], str):
                        try:
                            label = df.iloc[sub_row, 2]
                            freqs = [df.iloc[sub_row, i] for i in range(3, 7)]
                            percs = [df.iloc[sub_row + 1, i] for i in range(3, 7)]
                            sigs = df.iloc[sub_row + 2, 3:7].tolist()
                            rowdata = [label] + [f"{float(p)*100:.1f}% ({int(f)})" if pd.notna(p) and pd.notna(f) else "" for p, f in zip(percs, freqs)] + [", ".join([str(s) for s in sigs if pd.notna(s)])]
                            rows.append(rowdata)
                            sub_row += 3
                        except:
                            break
                    parsed_df = pd.DataFrame(rows, columns=["Metric"] + segments + ["Sig"])
                    tables.append((title, parsed_df))
                    row = sub_row
                else:
                    row += 1
            return tables

        parsed_tables = parse_wincross_tables(df)
        options = [f"Table {i+1}: {title[:40]}" for i, (title, _) in enumerate(parsed_tables)]
        selected_idx = st.selectbox("Select a table to preview", options=range(len(parsed_tables)), format_func=lambda x: options[x])
        selected_title, selected_df = parsed_tables[selected_idx]

        st.subheader(f"📘 {selected_title}")
        st.dataframe(selected_df)

        # GPT Analysis
        with st.spinner("Generating GPT insights..."):
            prompt = f"Analyze the following cross-tab table:
{selected_df.head(5).to_markdown()}
Provide key insights and business implications."
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior data strategist."},
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response.choices[0].message.content
            st.markdown("### 🧠 Executive Summary")
            st.markdown(summary)

        # Download Excel button
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            selected_df.to_excel(writer, index=False, sheet_name="Segment Table")
        excel_buffer.seek(0)
        st.download_button(
            label="📥 Download Segment Table (Excel)",
            data=excel_buffer,
            file_name="Segment_Table.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error reading sheet: {e}")
