
import streamlit as st

st.set_page_config(page_title="SAMI AI - Home", layout="wide")

st.title("🧠 Welcome to SAMI AI")
st.markdown("This is your all-in-one AI-powered research platform. Use the sidebar to access advanced analytical modules:")

# 🆕 Phase 1 CrossTabs Suite
st.sidebar.page_link("pages/CrossTabs_Analyzer_Phase1.py", label="📊 CrossTabs Analyzer Phase1")

# Legacy modules (optional)
with st.sidebar.expander("🗂 OLD Modules (Legacy)"):
    st.sidebar.page_link("pages/OLD_CrossTabs_Analyzer.py", label="📄 OLD CrossTabs Analyzer")
    st.sidebar.page_link("pages/OLD_CrossTabs_Step2.py", label="📄 OLD CrossTabs Step2")

# Other modules
st.sidebar.page_link("pages/CBC_Conjoint.py", label="📈 CBC Conjoint")
st.sidebar.page_link("pages/LCA_Module.py", label="📊 LCA Module")
st.sidebar.page_link("pages/MaxDiff_Module.py", label="📊 MaxDiff Module")
st.sidebar.page_link("pages/Persona_From_PPTX.py", label="🧬 Persona From PPTX")
st.sidebar.page_link("pages/Persona_Generator.py", label="🧠 Persona Generator")
st.sidebar.page_link("pages/SAMI_Analyzer.py", label="📊 SAMI Analyzer")
st.sidebar.page_link("pages/SEM_Module.py", label="📈 SEM Module")
st.sidebar.page_link("pages/Text_Analytics.py", label="📝 Text Analytics")
st.sidebar.page_link("pages/TURF_Module.py", label="📊 TURF Module")
