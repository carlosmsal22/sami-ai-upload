import streamlit as st
import pandas as pd
from io import BytesIO
import tempfile
from docx import Document
from openai import OpenAI
import os

# ============================== CONFIG ==============================
st.set_page_config(page_title="📊 CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

st.markdown("""
Upload your **WinCross-style Excel file** (Banner sheet), parse all tables, and receive executive summaries + export-ready tables.
""")

# ============================== UPLOAD ==============================
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    sheet_name = "Banner"
    xls = pd.ExcelFile(uploaded_file)
    if sheet_name not in xls.sheet_names:
        st.error("❌ 'Banner' sheet not found in file")
    else:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
        st.success("✅ File loaded successfully")

        # ============================== PARSER ==============================
        def parse_tables(df):
            segment_names = ["Group A", "Group B", "Group C", "Group D"]
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
                            sig_combined = ', '.join([
                                str(sig) for sig in sigs_raw if pd.notna(sig) and isinstance(sig, str)
                            ])
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

        tables = parse_tables(df)
        st.success(f"📈 Parsed {len(tables)} tables successfully")

        # ============================== ANALYSIS ==============================
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        for i, (title, table_df) in enumerate(tables):
            st.subheader(f"📘 Table {i+1}: {title}")
            st.dataframe(table_df, use_container_width=True)

            if st.button(f"🧠 Generate Insight for Table {i+1}"):
                with st.spinner("Sending to GPT for strategic summary..."):
                    try:
                        content_text = table_df.to_markdown(index=False)
                        prompt = f"""
You are a senior market research strategist. Analyze the following cross-tab table and provide a strategic executive summary.

Include:
1. Segment performance highlights
2. Key differences (based on Sig column)
3. Strategic implications for marketing, loyalty, or operations

Table Title: {title}

{content_text}
"""
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are a market insights strategist."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        insight = response.choices[0].message.content
                        st.markdown("### 💡 GPT Insight")
                        st.markdown(insight)
                    except Exception as e:
                        st.error(f"GPT error: {e}")

            # Export button
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                table_df.to_excel(writer, index=False, sheet_name="Formatted Table")
            excel_buffer.seek(0)
            st.download_button(
                label=f"⬇️ Download Table {i+1} (Excel)",
                data=excel_buffer,
                file_name=f"Table_{i+1}_{title[:20].replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
