import streamlit as st
import pandas as pd
from io import BytesIO
import re
import tempfile
import os
from openai import OpenAI

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("""
Upload your WinCross-style Excel file and generate deep insights + export-ready formatted tables.
""")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Banner", header=None)
    st.success("✅ Loaded 'Banner' sheet successfully")

    def parse_tables(df):
        segment_names = ["Frugal Basics", "Resourceful Savers", "Performance Enthusiasts", "Urban Techies"]
        tables = []
        row = 1
        while row < len(df):
            if "Table Title" in str(df.iloc[row, 1]):
                table_title = str(df.iloc[row + 1, 1])
                base_counts = df.iloc[row + 6, 3:7].tolist()
                segment_labels = [
                    f"{name} (n={int(count)})" if pd.notnull(count) else f"{name} (n=NA)"
                    for name, count in zip(segment_names, base_counts)
                ]
                table_rows = []
                sub_row = row + 8
                while sub_row + 2 < len(df) and isinstance(df.iloc[sub_row, 2], str):
                    metric_label = df.iloc[sub_row, 2]
                    try:
                        freqs = [df.iloc[sub_row, col] for col in range(3, 7)]
                        percs = [df.iloc[sub_row + 1, col] for col in range(3, 7)]
                        sigs_raw = df.iloc[sub_row + 2, 3:7].tolist()
                        values = [
                            f"{float(p)*100:.1f}% ({int(f)})"
                            if pd.notna(p) and pd.notna(f) and p != '-' and f != '-'
                            else ""
                            for p, f in zip(percs, freqs)
                        ]
                        sig_combined = ', '.join([str(sig) for sig in sigs_raw if pd.notna(sig) and isinstance(sig, str)])
                        table_rows.append([metric_label] + values + [sig_combined])
                    except:
                        break
                    sub_row += 3
                table_df = pd.DataFrame(table_rows, columns=["Metric"] + segment_labels + ["Sig"])
                tables.append((table_title, table_df))
                row = sub_row
            else:
                row += 1
        return tables

    def export_table(table_df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            table_df.to_excel(writer, sheet_name='Segment Table', index=False)
        output.seek(0)
        return output

    def gpt_summary(table_title, table_df):
        try:
            preview = table_df.head(4).to_markdown()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a research strategist analyzing crosstab tables."},
                    {"role": "user", "content": f"Here is a table titled '{table_title}'. Provide a summary of the key segment differences and strategic takeaways.\n\n{preview}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating GPT summary: {e}"

    tables = parse_tables(df)
    table_titles = [f"Table {i+1}: {t[0][:60]}" for i, t in enumerate(tables)]
    selected_idx = st.selectbox("Select a table to preview", options=range(len(tables)), format_func=lambda x: table_titles[x])

    # Display selected table
    table_title, table_df = tables[selected_idx]
    st.subheader(f"📘 {table_title}")
    st.dataframe(table_df, use_container_width=True)

    # GPT Summary
    st.subheader("🧠 Executive Summary")
    st.markdown(gpt_summary(table_title, table_df))

    # Export Button
    xls_bytes = export_table(table_df)
    st.download_button(
        "📥 Download Segment Table (Excel)",
        data=xls_bytes,
        file_name="Formatted_Segment_Table.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
