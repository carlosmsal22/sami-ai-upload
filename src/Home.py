import streamlit as st
import base64

# --- Configuration (Call ONCE at the top) ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI",
    initial_sidebar_state="collapsed" # Start collapsed
)

# --- Hosted Image URL ---
IMAGE_URL = "https://raw.githubusercontent.com/carlosmsal22/sami-ai-upload/main/images/robot-hand.png"

# --- Initialize Session State ---
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'landing'

# --- Helper Function to Show Combined Landing Page ---
# (This function remains the same as the previous version)
def show_landing_page_html(img_url):
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
    .get-started-button {{
        background-color: #03A9F4; color: white; border: none; padding: 10px 25px;
        border-radius: 5px; font-size: 1.0em; cursor: pointer;
        transition: background-color 0.3s ease; text-decoration: none; display: inline-block;
    }}
    .get-started-button:hover {{ background-color: #0288D1; }}
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
        <a href="/?start_app=true" class="get-started-button" target="_self">Get Started</a>
        </div></body></html>
    """
    st.components.v1.html(homepage_html, height=850, scrolling=False)


# --- Helper Function to Show Main App (NOW CENTERED with Prompt) ---
def show_main_app():
    # --- Use columns to center the main content ---
    col1, col_center, col3 = st.columns([1, 2, 1]) # Adjust ratios as needed ([1,3,1] etc.)

    with col_center:
        # Display centered content
        st.title("🤖 Welcome to SAMI AI")
        st.markdown("""
        Welcome to your all-in-one AI-powered research assistant.
        """) # Keep text shorter or use text-align center if needed

        st.info("👈 Click the arrow in the upper-left corner to expand the sidebar and access the analysis modules.", icon="ℹ️")

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

    # --- Main Area Content (Placeholder for Module Logic) ---
    # This will now appear below the centered welcome message if a module is selected
    # If you want modules ALSO centered, wrap this section in columns too.
    if 'current_module' in st.session_state:
        # Example: Displaying module content (currently not centered)
        st.header(f"Module: {st.session_state.current_module}")
        st.info("Module content goes here...")
        # Add your specific module UI elements here based on st.session_state.current_module


# --- Page Routing Logic (Cleaned) ---
if st.query_params.get("start_app") == "true":
    st.session_state.view_state = 'app'
    st.query_params.clear()

current_state = st.session_state.get('view_state', 'landing')

if current_state == 'app':
    show_main_app()
elif current_state == 'landing':
    show_landing_page_html(IMAGE_URL)
else:
    st.session_state.view_state = 'landing'
    st.rerun()
