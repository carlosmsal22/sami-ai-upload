
import streamlit as st
import pandas as pd
from io import BytesIO
import re
import os
from openai import OpenAI

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")
st.markdown("Upload your WinCross-style Excel file and generate banner-point comparisons with exportable insights.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Banner", header=None)
        st.success("✅ Loaded 'Banner' sheet successfully!")
        st.dataframe(df.head(10))

        data_start = None
        for i in range(len(df)):
            if isinstance(df.iloc[i, 2], str) and "Table Title" in df.iloc[i, 1]:
                data_start = i + 1
                break

        if data_start is None:
            st.warning("Could not locate banner table structure.")
        else:
            table_title = str(df.iloc[data_start, 1])
            base_counts = df.iloc[data_start+5, 3:7].tolist()
            banners = [
                f"{label} (n={int(b)})" if pd.notnull(b) else label
                for label, b in zip(["Group A", "Group B", "Group C", "Group D"], base_counts)
            ]

            rows = []
            sub_row = data_start + 7
            while sub_row + 2 < len(df) and isinstance(df.iloc[sub_row, 2], str):
                label = df.iloc[sub_row, 2]
                try:
                    freqs = [df.iloc[sub_row, i] for i in range(3, 7)]
                    percs = [df.iloc[sub_row+1, i] for i in range(3, 7)]
                    sigs = df.iloc[sub_row+2, 3:7].tolist()
                    values = [f"{float(p)*100:.1f}% ({int(f)})" if pd.notna(p) and pd.notna(f) else "" for p, f in zip(percs, freqs)]
                    sigs_joined = ', '.join([str(s) for s in sigs if pd.notna(s)])
                    rows.append([label] + values + [sigs_joined])
                except:
                    break
                sub_row += 3

            table_df = pd.DataFrame(rows, columns=["Metric"] + banners + ["Sig"])
            st.subheader(f"📘 {table_title}")
            st.dataframe(table_df, use_container_width=True)

            gpt_prompt = f"""
You are a senior research analyst. Review this contingency table comparing banner groups (e.g., job roles, regions, etc.). Summarize major patterns, differences, and any statistically significant variations across groups. Suggest possible explanations.

{table_df.head(5).to_markdown()}
""".strip()

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a market research strategist."},
                        {"role": "user", "content": gpt_prompt}
                    ]
                )
                st.subheader("💡 Executive Summary")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"GPT error: {e}")

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                table_df.to_excel(writer, index=False, sheet_name="Segment Table")
            output.seek(0)
            st.download_button("📥 Download Segment Table (Excel)", output, file_name="formatted_segment_table.xlsx")

    except Exception as e:
        st.error(f"Failed to load file: {e}")
