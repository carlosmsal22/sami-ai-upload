import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO
from utils.parsers import parse_crosstab_file
from utils.gpt_helpers import generate_gpt_summary

st.set_page_config(page_title="📊 Cross-Tabs Analyzer", layout="wide")
st.title("📊 Cross-Tabs Analyzer + GPT Insight Summarizer")

uploaded_file = st.file_uploader("Upload a crosstab Excel file", type=["xlsx"])

if uploaded_file:
    st.info("Parsing file and detecting headers...")
    try:
        df = parse_crosstab_file(uploaded_file)
        st.success("✅ File parsed successfully.")
        st.dataframe(df)

        # Group comparison chart
        st.subheader("📉 Group Comparison Chart")
        try:
            group_cols = df.columns[1:]
            melted = df.melt(id_vars=[df.columns[0]], value_vars=group_cols,
                             var_name="Group", value_name="Value")
            melted = melted.dropna()
            melted["Value"] = pd.to_numeric(melted["Value"], errors="coerce")

            fig, ax = plt.subplots(figsize=(10, 6))
            for label, grp in melted.groupby(df.columns[0]):
                ax.plot(grp["Group"], grp["Value"], marker="o", label=label)
            ax.set_ylabel("Value (%)")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error generating chart: {e}")

        # GPT Summary
        if st.button("🧠 Generate GPT Summary"):
            st.subheader("🧠 GPT Insights Summary")
            try:
                summary = generate_gpt_summary(df)
                st.markdown(summary)
            except Exception as e:
                st.error(f"❌ Error with GPT: {e}")

    except Exception as e:
        st.error(f"❌ Error parsing file: {e}")
