import streamlit as st

st.set_page_config(page_title="SAMI AI Home", layout="wide")

st.title("🤖 Welcome to SAMI AI – Insights Platform")

st.markdown("""
This is your all-in-one AI-powered research platform.  
Use the sidebar to access advanced analytical modules:
""")

st.sidebar.page_link("pages/CBC_Conjoint.py", label="📦 CBC Conjoint")
st.sidebar.page_link("pages/CrossTabs_Analyzer.py", label="📊 Cross-Tabs Analyzer")
st.sidebar.page_link("pages/MaxDiff_Module.py", label="📊 MaxDiff Module")
st.sidebar.page_link("pages/TURF_Module.py", label="🌱 TURF Module")
st.sidebar.page_link("pages/Text_Analytics.py", label="📝 Text Analytics")
st.sidebar.page_link("pages/Persona_Generator.py", label="🎯 Persona Generator")
st.sidebar.page_link("pages/Persona_From_PPTX.py", label="🧠 Persona From PPTX")
st.sidebar.page_link("pages/SAMI_Analyzer.py", label="📈 SAMI Analyzer")
st.sidebar.page_link("pages/SEM_Module.py", label="📐 SEM Module")
