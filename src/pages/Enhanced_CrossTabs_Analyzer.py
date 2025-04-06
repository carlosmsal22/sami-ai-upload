import streamlit as st
import pandas as pd
from io import BytesIO
import re
from openai import OpenAI
import os

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload WinCross-Style Excel File", type=["xlsx"])
if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        if "Banner" not in xls.sheet_names:
            st.error("❌ Could not find sheet named 'Banner'")
        else:
            df = pd.read_excel(uploaded_file, sheet_name="Banner", header=None)
            st.success("✅ Loaded 'Banner' sheet successfully")

            # Parse tables from "Banner"
            def extract_tables(df):
                tables = []
                i = 0
                while i < len(df):
                    if isinstance(df.iloc[i, 1], str) and "Table Title" in df.iloc[i, 1]:
                        title = df.iloc[i + 1, 1]
                        base_counts = df.iloc[i + 6, 3:7].tolist()
                        labels = [
                            f"{n} (n={int(c)})" if pd.notnull(c) else f"{n} (n=NA)"
                            for n, c in zip(["Frugal Basics", "Resourceful Savers", "Performance Enthusiasts", "Urban Techies"], base_counts)
                        ]
                        rows = []
                        r = i + 8
                        while r + 2 < len(df) and isinstance(df.iloc[r, 2], str):
                            label = df.iloc[r, 2]
                            try:
                                freqs = [df.iloc[r, j] for j in range(3, 7)]
                                percs = [df.iloc[r + 1, j] for j in range(3, 7)]
                                sigs = df.iloc[r + 2, 3:7].tolist()
                                values = [
                                    f"{float(p)*100:.1f}% ({int(f)})"
                                    if pd.notna(p) and pd.notna(f) else ""
                                    for p, f in zip(percs, freqs)
                                ]
                                sig_text = ", ".join([str(s) for s in sigs if isinstance(s, str)])
                                rows.append([label] + values + [sig_text])
                            except:
                                break
                            r += 3
                        tdf = pd.DataFrame(rows, columns=["Metric"] + labels + ["Sig"])
                        tables.append((title, tdf))
                        i = r
                    else:
                        i += 1
                return tables

            tables = extract_tables(df)
            if not tables:
                st.warning("⚠️ No valid tables extracted.")
            else:
                options = [f"Table {i+1}: {title[:40]}" for i, (title, _) in enumerate(tables)]
                selected = st.selectbox("Select a table to preview", range(len(tables)), format_func=lambda i: options[i])
                title, tdf = tables[selected]
                st.subheader(f"📘 {title}")
                st.dataframe(tdf)

                # GPT Summary
                try:
                    st.markdown("### 🧠 Executive Summary")
                    gpt_prompt = f"""You are an executive insight generator. Analyze this cross-tab table and summarize key differences across segments.

{tdf.to_markdown()}"""
                    with st.spinner("Generating GPT summary..."):
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a senior research strategist."},
                                {"role": "user", "content": gpt_prompt}
                            ]
                        )
                        st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"GPT Error: {e}")

                # Export
                st.download_button(
                    "📥 Download Segment Table (Excel)",
                    data=tdf.to_csv(index=False),
                    file_name=f"{title.replace(' ', '_')}.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
