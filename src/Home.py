import streamlit as st

# --- Configuration (Sidebar starts expanded) ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI"
)

# --- Hosted Image URL ---
IMAGE_URL = "https://raw.githubusercontent.com/carlosmsal22/sami-ai-upload/main/images/robot-hand.png"

# --- Initialize Session State ---
if 'current_module' not in st.session_state:
    st.session_state.current_module = None

# --- Helper Function to Show Landing Page HTML Component ---
def show_landing_page_html(img_url):
    # (Content of this function remains exactly the same as the previous version)
    # ... (CSS and HTML for the landing page component) ...
    inlined_css = f"""
    body {{
        font-family: 'Roboto', sans-serif; margin: 0; color: #E0E0E0;
        display: flex; align-items: center; justify-content: center;
        min-height: 98vh; box-sizing: border-box;
        background-image: url('{img_url}'); background-size: cover;
        background-position: center center; background-repeat: no-repeat;
        background-attachment: fixed; overflow: hidden;
    }}
    .content-container {{
        background-color: rgba(0, 0, 0, 0.6); max-width: 500px;
        padding: 35px 45px; border-radius: 8px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4); width: 85%;
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }}
    header {{
        position: absolute; top: 20px; left: 0; width: 100%; padding: 0 40px;
        display: flex; justify-content: space-between; align-items: center;
        box-sizing: border-box; z-index: 10;
    }}
    .logo {{ font-size: 1.4em; font-weight: bold; color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }}
    nav a {{ color: #BBDEFB; text-decoration: none; margin-left: 20px; font-size: 1em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);}}
    nav a:hover {{ color: #FFFFFF; text-decoration: underline; }}
    h1 {{ font-size: 2.4em; margin-bottom: 10px; color: #FFFFFF; }}
    .subtitle {{ font-size: 1.1em; color: #B0BEC5; margin-bottom: 20px; font-weight: 400; }}
    .description {{ line-height: 1.5; margin-bottom: 25px; font-size: 0.9em; color: #ECEFF1;}}
    .prompt {{ font-size: 0.9em; margin-top: 30px; color: #B0BEC5; }}
    @media (max-width: 768px) {{
        body {{ background-attachment: scroll; overflow: auto; min-height: 100vh; }}
        header {{ position: static; flex-direction: column; text-align: center; margin-bottom: 20px; background-color: rgba(0,0,0,0.5); border-radius: 5px; padding: 10px; }}
        nav {{ margin-top: 10px; }}
        nav a {{ margin: 0 10px; }}
        .content-container {{ padding: 25px 15px; max-width: 90%; margin-top: 0; }}
        h1 {{ font-size: 2.0em; }}
        .subtitle {{ font-size: 1.0em; }}
        .description {{ font-size: 0.9em; }}
    }}
    """
    homepage_html = f"""
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAMI AI</title><style>{inlined_css}</style>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    </head><body><header><div class="logo">Insights AI</div><nav>
        <a href="#">Register</a><a href="#">Login</a></nav></header>
        <div class="content-container"><h1>SAMI AI</h1>
        <p class="subtitle">EMPOWERING FUTURE TRENDS</p>
        <p class="description">Get AI-driven insights on emerging trends in markets, technology, and consumer behavior. Ask questions, explore categorized responses, and easily save or export your findings.</p>
        <p class="prompt"><i>Select a module from the sidebar to begin.</i></p>
        </div></body></html>
    """
    st.components.v1.html(homepage_html, height=850, scrolling=False)
    # Add a debug print *after* the component call too
    st.write("DEBUG: Finished rendering HTML component")


# --- Define Module Content Area ---
# (This function remains the same)
def show_module_content(module_key):
    # (Content for modules, e.g., SAMI analyzer)
    # ...
    if module_key == "SAMI": # Example for SAMI Analyzer
         st.subheader("📊 SAMI AI - Advanced Analytics Suite")
         st.caption("Upload your dataset and discover actionable insights.")
         uploaded_file = st.file_uploader("Upload your dataset", type=['csv', 'xlsx'], key=f"upload_{module_key}") # Unique key per module instance
         if uploaded_file:
              st.success(f"File '{uploaded_file.name}' uploaded.")
         st.text_input("Ask a question about your data:", placeholder="E.g. What are the key drivers of satisfaction?", key=f"question_{module_key}")
         st.markdown("---")
         col1, col2, col3 = st.columns(3)
         with col1: st.checkbox("📈 Correlation Matrix", key=f"corr_{module_key}")
         with col1: st.checkbox("📊 Distributions", key=f"dist_{module_key}")
         with col2: st.checkbox("🌀 PCA Projection", key=f"pca_{module_key}")
         with col2: st.checkbox("🧩 Clustering", key=f"clust_{module_key}")
         with col3: st.checkbox("📝 Text Analysis (Coming Soon)", disabled=True, key=f"text_{module_key}")
         with col3: st.checkbox("⚠️ Anomaly Detection", key=f"anomaly_{module_key}")
         st.markdown("---")
         with st.expander("ℹ️ How to use this tool"): st.write("Instructions go here...")
         st.button("🚀 Run Analysis", type="primary", key=f"run_{module_key}")
    else:
         st.header(f"Module: {module_key}")
         st.info("Module content goes here...")
    st.write(f"DEBUG: Finished rendering module content for {module_key}")


# --- Sidebar Definition ---
# (Remains the same)
with st.sidebar:
    # ... (Home button and module buttons) ...
    if st.button("🏠 Home", key="btn_home", help="Return to Landing Page"):
        st.session_state.current_module = None
        st.write("DEBUG: Home button clicked, setting current_module to None") # DEBUG
        st.rerun()
    st.markdown("---")
    st.subheader("Analysis Modules")
    module_buttons = { # ... (module names and keys) ...
        "CBC Conjoint": "CBC", "CrossTabs Analyzer Phase1": "CrossTabs1",
        "Enhanced CrossTabs Analyzer": "CrossTabs2", "Executive Insight Generator old": "ExecOld",
        "LCA Module": "LCA", "MaxDiff Module": "MaxDiff", "OLD CrossTabs Analyzer": "OldCrossTabs1",
        "OLD CrossTabs Step2": "OldCrossTabs2", "Persona From PPTX": "PersonaPPTX",
        "Persona Generator": "PersonaGen", "SAMI Analyzer": "SAMI", "SEM Module": "SEM",
        "Text Analytics": "Text", "TURF Module": "TURF"
    }
    for label, key in module_buttons.items():
        if st.button(label, key=f"btn_{key}"):
            st.session_state.current_module = key
            st.write(f"DEBUG: Module button '{label}' clicked, setting current_module to {key}") # DEBUG
            st.rerun()
    st.markdown("---")
    st.subheader("Analysis Settings")
    analysis_mode = st.radio("Analysis Mode", ["Basic EDA", "Advanced Insights", "Predictive Modeling"], key="analysis_mode_radio")
    with st.expander("Advanced options"):
         st.write("Advanced settings here...")


# --- Main Area Logic ---
selected_module = st.session_state.get('current_module', None)

# --- ADDED DEBUGGING HERE ---
st.write(f"DEBUG: Checking routing. Value of selected_module: {selected_module} (Type: {type(selected_module)})")

if selected_module is None:
    st.write("DEBUG: Condition 'selected_module is None' is TRUE. Calling show_landing_page_html...") # DEBUG
    show_landing_page_html(IMAGE_URL)
else:
    st.write(f"DEBUG: Condition 'selected_module is None' is FALSE. Calling show_module_content with key: {selected_module}") # DEBUG
    show_module_content(selected_module)

st.write("--- End of Script Execution ---") # DEBUG
