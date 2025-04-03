# Home.py – Main Landing Page for SAMI AI Streamlit App
import streamlit as st

st.set_page_config(page_title="SAMI AI Home", layout="wide")

st.title("🤖 Welcome to SAMI AI Advanced Analytical Tool")

st.markdown("""
Welcome to the SAMI AI platform. Explore our suite of powerful modules:

- 📊 **Executive Insight Generator**: Upload cross-tab files, generate GPT-style summaries and visual charts.
- 🧮 **CBC Conjoint Analyzer**: Simulate consumer preferences using choice-based conjoint.
- 📈 **MaxDiff Analysis Module**: Identify what matters most to your customers.
- 🌐 **TURF Analysis Tool**: Optimize your product mix for maximum reach.
- 📚 **LCA & SEM Models**: Dive into latent class and structural modeling.

Use the sidebar to navigate between modules.
""")

st.sidebar.header("Navigation")
st.sidebar.page_link("pages/Executive_Insight_Generator.py", label="📊 Executive Insight Generator")
st.sidebar.page_link("pages/CBC_Conjoint.py", label="🧮 CBC Conjoint Analyzer")
st.sidebar.page_link("pages/MaxDiff_Analyzer.py", label="📈 MaxDiff Analysis")
st.sidebar.page_link("pages/TURF_Analyzer.py", label="🌐 TURF Analyzer")
st.sidebar.page_link("pages/LCA_Model.py", label="📚 Latent Class Analysis")
st.sidebar.page_link("pages/SEM_Model.py", label="📚 Structural Equation Modeling")