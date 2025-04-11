import streamlit as st

# --- Configuration (Sidebar starts expanded) ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI"
    # REMOVED: initial_sidebar_state="collapsed"
)

# --- Hosted Image URL ---
IMAGE_URL = "https://raw.githubusercontent.com/carlosmsal22/sami-ai-upload/main/images/robot-hand.png"

# --- Initialize Session State ---
# 'current_module' will store the key of the selected module, or None for landing
if 'current_module' not in st.session_state:
    st.session_state.current_module = None # Start on the landing/home view

# --- Inject CSS for Background (Apply ONLY when on landing view) ---
def set_landing_background(img_url):
    css = f"""
    <style>
    /* Target the Streamlit app container - more specific than body */
    [data-testid="stAppViewContainer"] > .main > div:first-child {{
        background-image: url('{img_url}');
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* Make header potentially transparent over background */
     [data-testid="stHeader"] {{
        background: rgba(0,0,0,0); /* Transparent background */
        color: white; /* Assuming dark background, make header text white */
    }}
     [data-testid="stHeader"] [data-testid="stWidgetLabel"] a {{
         color: white; /* Style links in header if any */
     }}
     /* Style the overlay text container if needed */
     .landing-content {{
        background-color: rgba(0, 0, 0, 0.6);
        max-width: 500px;
        padding: 35px 45px;
        border-radius: 8px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #E0E0E0; /* Text color for overlay */
        margin: auto; /* Center the box */
        margin-top: 15vh; /* Adjust vertical position */
     }}
     .landing-content h1 {{ color: #FFFFFF; font-size: 2.4em; margin-bottom: 10px;}}
     .landing-content p {{ color: #ECEFF1; line-height: 1.5; font-size: 0.9em; }}
     .landing-content .subtitle {{ color: #B0BEC5; font-size: 1.1em; margin-bottom: 20px; font-weight: 400; }}
     /* Hide default Streamlit elements ONLY on landing page */
     [data-testid="stSidebar"] + [data-testid="stAppViewContainer"] [data-testid="stHeader"] {{
         /* This tries to hide the header only when sidebar is present and we are in landing */
         /* Might need adjustment based on Streamlit version / DOM structure */
        visibility: hidden;
     }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Define Landing Page Content (using native elements) ---
def show_landing_content():
    # Use columns to help center the overlay box vertically/horizontally
    col1, col_center, col3 = st.columns([1, 2, 1])
    with col_center:
        # Use st.markdown with class for styling via CSS above
        st.markdown(
            """
            <div class="landing-content">
                <h1>SAMI AI</h1>
                <p class="subtitle">EMPOWERING FUTURE TRENDS</p>
                <p>Get AI-driven insights on emerging trends in markets, technology, and consumer behavior. Ask questions, explore categorized responses, and easily save or export your findings.</p>
                <p style="font-size: 0.8em; margin-top: 30px;"><i>Select a module from the sidebar to begin.</i></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    # Add placeholder elements to push content down if needed (adjust spacer height)
    # st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)


# --- Define Module Content Area ---
def show_module_content(module_key):
    if module_key == "SAMI": # Example for SAMI Analyzer
         # Use screenshot 750 as a guide for the required layout
         st.subheader("📊 SAMI AI - Advanced Analytics Suite") # Example Title
         st.caption("Upload your dataset and discover actionable insights.")

         # File Uploader
         uploaded_file = st.file_uploader("Upload your dataset", type=['csv', 'xlsx'])
         if uploaded_file:
              st.success(f"File '{uploaded_file.name}' uploaded.")
              # Add logic to load/process file (e.g., df = pd.read_csv(uploaded_file))

         # Input field
         st.text_input("Ask a question about your data:", placeholder="E.g. What are the key drivers of satisfaction?")

         st.markdown("---") # Separator

         # Analysis Options (use columns for layout)
         col1, col2, col3 = st.columns(3)
         with col1:
             st.checkbox("📈 Correlation Matrix")
             st.checkbox("📊 Distributions")
         with col2:
             st.checkbox("🌀 PCA Projection")
             st.checkbox("🧩 Clustering")
         with col3:
             st.checkbox("📝 Text Analysis (Coming Soon)", disabled=True)
             st.checkbox("⚠️ Anomaly Detection")

         st.markdown("---")

         # How to use expander
         with st.expander("ℹ️ How to use this tool"):
              st.write("Instructions go here...")

         # Run button
         st.button("🚀 Run Analysis", type="primary")

    else:
         # Default for other modules
         st.header(f"Module: {module_key}")
         st.info("Module content goes here...")


# --- Sidebar Definition ---
with st.sidebar:
    # Home Button - sets current_module to None
    if st.button("🏠 Home", key="btn_home", help="Return to Landing Page"):
        st.session_state.current_module = None
        st.rerun() # Rerun to reflect the change

    st.markdown("---")
    st.subheader("Analysis Modules")
    module_buttons = {
        "CBC Conjoint": "CBC", "CrossTabs Analyzer Phase1": "CrossTabs1",
        "Enhanced CrossTabs Analyzer": "CrossTabs2", "Executive Insight Generator old": "ExecOld",
        "LCA Module": "LCA", "MaxDiff Module": "MaxDiff", "OLD CrossTabs Analyzer": "OldCrossTabs1",
        "OLD CrossTabs Step2": "OldCrossTabs2", "Persona From PPTX": "PersonaPPTX",
        "Persona Generator": "PersonaGen", "SAMI Analyzer": "SAMI", "SEM Module": "SEM",
        "Text Analytics": "Text", "TURF Module": "TURF"
    }
    for label, key in module_buttons.items():
        # When a module button is clicked, store its key
        if st.button(label, key=f"btn_{key}"):
            st.session_state.current_module = key
            st.rerun() # Rerun to show the selected module

    # --- Add Analysis Settings from screenshot 750 ---
    st.markdown("---")
    st.subheader("Analysis Settings")
    analysis_mode = st.radio("Analysis Mode", ["Basic EDA", "Advanced Insights", "Predictive Modeling"])
    with st.expander("Advanced options"):
         st.write("Advanced settings here...")


# --- Main Area Logic ---
selected_module = st.session_state.get('current_module', None)

if selected_module is None:
    # Show landing page content
    set_landing_background(IMAGE_URL) # Apply background CSS
    show_landing_content()
else:
    # Show the selected module's content
    # Don't apply landing background CSS here
    show_module_content(selected_module)
