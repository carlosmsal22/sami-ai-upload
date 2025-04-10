import streamlit as st
import base64

# --- Configuration (Call ONCE at the top) ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed
)

# --- Hosted Image URL ---
IMAGE_URL = "https://raw.githubusercontent.com/carlosmsal22/sami-ai-upload/main/images/robot-hand.png"

# --- Initialize Session State ---
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'landing'

# --- DEBUGGING: Show current state at the start of each run ---
st.write(f"DEBUGGING: Current view_state at start: {st.session_state.get('view_state', 'Not Set')}")


# --- Helper Function to Show Combined Landing Page ---
def show_landing_page_html(img_url):
    st.write("DEBUGGING: Entering show_landing_page_html()")

    # --- Modified CSS (Overlay Box Adjustments) ---
    inlined_css = f"""
    body {{
        font-family: 'Roboto', sans-serif; margin: 0; color: #E0E0E0;
        display: flex; align-items: center; justify-content: center;
        min-height: 98vh; box-sizing: border-box;
        background-image: url('{img_url}'); background-size: cover;
        background-position: center center; background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .content-container {{
        /* --- ADJUSTMENTS HERE --- */
        background-color: rgba(0, 0, 0, 0.6); /* Slightly more transparent */
        max-width: 550px; /* Narrower box */
        /* --- End Adjustments --- */
        padding: 40px 50px; /* Adjusted padding slightly */
        border-radius: 8px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        width: 90%; text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    header {{
        position: absolute; top: 20px; left: 0; width: 100%; padding: 0 40px;
        display: flex; justify-content: space-between; align-items: center;
        box-sizing: border-box; z-index: 10;
    }}
    .logo {{ font-size: 1.4em; font-weight: bold; color: #FFFFFF; }}
    nav a {{ color: #BBDEFB; text-decoration: none; margin-left: 20px; font-size: 1em; }}
    nav a:hover {{ color: #FFFFFF; text-decoration: underline; }}
    h1 {{ font-size: 2.6em; /* Slightly smaller */ margin-bottom: 10px; color: #FFFFFF; }}
    .subtitle {{ font-size: 1.2em; /* Slightly smaller */ color: #B0BEC5; margin-bottom: 25px; font-weight: 400; }}
    .description {{ line-height: 1.6; margin-bottom: 30px; font-size: 0.95em; /* Slightly smaller */ color: #ECEFF1;}}
    .get-started-button {{
        background-color: #03A9F4; color: white; border: none; padding: 12px 28px;
        border-radius: 5px; font-size: 1.1em; cursor: pointer;
        transition: background-color 0.3s ease; text-decoration: none; display: inline-block;
    }}
    .get-started-button:hover {{ background-color: #0288D1; }}
    @media (max-width: 768px) {{
        header {{ padding: 0 20px; flex-direction: column; text-align: center; position: static; margin-bottom: 30px; background-color: rgba(0,0,0,0.5); border-radius: 5px; padding: 10px; }}
        nav {{ margin-top: 10px; }}
        nav a {{ margin: 0 10px; }}
        .content-container {{ padding: 30px 20px; max-width: 90%; /* Adjust width for mobile */}}
        h1 {{ font-size: 2.0em; }}
        .subtitle {{ font-size: 1.0em; }}
        .description {{ font-size: 0.9em; }}
        body {{ background-attachment: scroll; }}
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
        <a href="/?start_app=true" class="get-started-button" target="_self">Get Started</a>
        </div></body></html>
    """
    st.components.v1.html(homepage_html, height=750, scrolling=False)
    st.write("DEBUGGING: Exiting show_landing_page_html()")


# --- Helper Function to Show Main App ---
def show_main_app():
    st.write("DEBUGGING: Entering show_main_app()")

    # --- Use columns to center the title and welcome text ---
    col1, col2, col3 = st.columns([1, 2, 1]) # Adjust ratios (e.g., [1,3,1] for wider center)
    with col2:
        st.title("🤖 Welcome to SAMI AI")
        st.markdown("""
        Welcome to your all-in-one AI-powered research assistant.
        Use the sidebar to explore and analyze your data using advanced modules:
        """)
    # --- End centering ---

    # --- Sidebar Definition (Remains the same) ---
    with st.sidebar:
        st.page_link("Home.py", label="Home", icon="🏠")
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
            if st.button(label, key=f"btn_{key}"):
                st.session_state.current_module = key
                st.write(f"DEBUGGING: Sidebar button '{label}' clicked, current_module set to: {key}")

    # --- Main Area Content (Placeholder for Module Logic) ---
    # Display module content if selected, otherwise the centered welcome message stays visible
    if 'current_module' in st.session_state:
         # Use columns again if you want module content centered too, otherwise it fills normally
        col1_m, col2_m, col3_m = st.columns([1, 2, 1]) # Example centering for module content
        with col2_m:
            st.write(f"DEBUGGING: Displaying content for module: {st.session_state.current_module}")
            st.header(f"Module: {st.session_state.current_module}")
            st.info("Module content goes here...")
    else:
        st.write("DEBUGGING: No module selected yet (Welcome message shown centered).")

    st.write("DEBUGGING: Exiting show_main_app()")


# --- Page Routing Logic (Remains the same) ---
if st.query_params.get("start_app") == "true":
    st.write("DEBUGGING: Query param 'start_app=true' detected.")
    st.session_state.view_state = 'app'
    st.query_params.clear()
    st.write(f"DEBUGGING: view_state set to 'app', query params cleared.")

current_state = st.session_state.get('view_state', 'landing')
st.write(f"DEBUGGING: Routing based on view_state: {current_state}")

if current_state == 'app':
    show_main_app()
elif current_state == 'landing':
    show_landing_page_html(IMAGE_URL)
else:
    st.error(f"DEBUGGING: Invalid view_state encountered: {current_state}")
    st.session_state.view_state = 'landing'
    st.rerun()

# --- Optional: Hide Streamlit Elements (Remains commented out for now) ---
# ...
