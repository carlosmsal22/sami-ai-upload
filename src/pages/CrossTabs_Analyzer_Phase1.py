
import streamlit as st
import pandas as pd
import openai
import os
from io import BytesIO

st.set_page_config(page_title="📊 Enhanced CrossTabs Analyzer", layout="wide")
st.title("📊 Enhanced CrossTabs Analyzer")

st.markdown("Upload your WinCross-style Excel file and generate banner-point comparisons with exportable insights.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    try:
        sheet_name = "Banner"
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
        st.success("✅ Loaded 'Banner' sheet successfully!")

        # Preview table
        st.dataframe(df.head(10), use_container_width=True)

        # Extract a sample data row (after finding the real data start)
        start_row = None
        for i in range(len(df)):
            if df.iloc[i].isna().sum() < len(df.columns) - 2:
                start_row = i
                break

        if start_row is not None:
            data_section = df.iloc[start_row:]
            data_section.columns = [str(c) for c in range(data_section.shape[1])]
            data_section.reset_index(drop=True, inplace=True)

            st.subheader("📘 Table Preview")
            st.dataframe(data_section.head(5))

            # Prompt GPT for interpretation
            gpt_input = data_section.head(10).to_string(index=False)

            st.subheader("💡 Executive Summary")
            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")
                messages = [
                    {
                        "role": "system",
                        "content": "You are a senior market research analyst. Analyze the following crosstab and provide insights in plain English."
                    },
                    {
                        "role": "user",
                        "content": f"Here is the table:
{gpt_input}"
                    }
                ]

                with st.spinner("Analyzing with GPT..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    insight = response.choices[0].message.content
                    st.markdown(insight)

            except Exception as e:
                st.error(f"GPT error: {e}")

            # Download cleaned table
            output = BytesIO()
            data_section.to_excel(output, index=False)
            output.seek(0)
            st.download_button(
                label="📥 Download Segment Table (Excel)",
                data=output,
                file_name="Formatted_Segment_Table.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("❗ Could not detect where the data starts. Please ensure your Excel table is properly formatted.")

    except Exception as e:
        st.error(f"Failed to load file: {e}")
