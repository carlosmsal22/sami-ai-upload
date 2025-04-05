import streamlit as st

st.set_page_config(page_title="SAMI AI – Insights Platform", layout="wide")

st.title("🤖 Welcome to SAMI AI")

st.markdown("""
Welcome to your all-in-one AI-powered research assistant.  
Use the sidebar to explore and analyze your data using advanced modules:

### Available Modules:
- 🧠 **SAMI Analyzer** – GPT-enhanced EDA and visualization
- 📦 **CBC Conjoint** – Run choice-based modeling simulations
- 🎯 **MaxDiff Module** – Prioritization using MaxDiff scaling
- 🎯 **TURF Module** – Find optimal feature combinations
- 🔍 **Text Analytics** – Extract insights from open-ended responses
- 🧬 **LCA Module** – Latent Class segmentation
- 🔗 **SEM Module** – Structural Equation Modeling
- 📊 **CrossTabs Analyzer Phase 1** – Frequency, significance tests & stat tables
- 📈 **CrossTabs Analyzer Phase 2** – GPT-based executive summary of crosstabs
- 📄 **Executive Insight Generator** – Create slide-ready insight summaries
- 🧬 **Persona Generator** – Extract buyer personas from segmentation
- 🧬 **Persona From PPTX** – Generate personas from uploaded PPTX files

---

💡 Upload your data in the respective module and let SAMI AI do the heavy lifting.
""")
