import streamlit as st
import base64

# --- Configuration (Call ONCE at the top) ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed
)

# --- Hosted Image URL ---
# Use the raw GitHub content URL:
IMAGE_URL = "https://raw.githubusercontent.com/carlosmsal22/sami-ai-upload/main/images/robot-hand.png"

# --- Initialize Session State ---
# Only two states needed now: 'landing' and 'app'
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'landing' # Start with the combined landing page

# --- DEBUGGING: Show current state at the start of each run ---
st.write(f"DEBUGGING: Current view_state at start: {st.session_state.get('view_state', 'Not Set')}")


# --- Helper Function to Show Combined Landing Page (Image Background + Content) ---
def show_landing_page_html(img_url):
    st.write("DEBUGGING: Entering show_landing_page_html()") # Debug print

    # --- Modified CSS ---
    inlined_css = f"""
    body {{
        font-family: 'Roboto', sans-serif; margin: 0; color: #E0E0E0; /* Lighter text for dark background */
        display: flex; align-items: center; justify-content: center;
        min-height: 98vh; /* Slightly less than 100vh to avoid scrollbars sometimes */
        box-sizing: border-box;
        /* --- Background Image Styles --- */
        background-image: url('{img_url}');
        background-size: cover; /* Cover the entire viewport */
        background-position: center center; /* Center the image */
        background-repeat: no-repeat;
        background-attachment: fixed; /* Keep background fixed during scroll (optional) */
    }}
    .content-container {{
        /* Make the box semi-transparent dark */
        background-color: rgba(0, 0, 0, 0.65); /* Dark semi-transparent */
        padding: 40px 60px;
        border-radius: 8px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        max-width: 700px;
        width: 90%;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle border */
    }}
    header {{
        /* Position header relative to viewport */
        position: absolute; top: 20px; left: 0; width: 100%; padding: 0 40px;
        display: flex; justify-content: space-between; align-items: center;
        box-sizing: border-box; z-index: 10;
    }}
    /* Adjust header text/link colors for dark background */
    .logo {{ font-size: 1.4em; font-weight: bold; color: #FFFFFF; }}
    nav a {{ color: #BBDEFB; /* Light blue links */ text-decoration: none; margin-left: 20px; font-size: 1em; }}
    nav a:hover {{ color: #FFFFFF; text-decoration: underline; }}

    /* Adjust content text colors */
    h1 {{ font-size: 2.8em; margin-bottom: 10px; color: #FFFFFF; }}
    .subtitle {{ font-size: 1.3em; color: #B0BEC5; /* Light grey */ margin-bottom: 25px; font-weight: 400; }}
    .description {{ line-height: 1.6; margin-bottom: 30px; font-size: 1em; color: #ECEFF1; /* Off-white */}}

    .get-started-button {{
        background-color: #03A9F4; /* Bright blue button */
        color: white; border: none; padding: 12px 28px; border-radius: 5px;
        font-size: 1.1em; cursor: pointer; transition: background-color 0.3s ease;
        text-decoration: none; display: inline-block;
    }}
    .get-started-button:hover {{ background-color: #0288D1; /* Darker blue on hover */ }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        header {{ padding: 0 20px; flex-direction: column; text-align: center; position: static; margin-bottom: 30px; background-color: rgba(0,0,0,0.5); /* Add bg on mobile */ border-radius: 5px; padding: 10px; }}
        nav {{ margin-top: 10px; }}
        nav a {{ margin: 0 10px; }}
        .content-container {{ padding: 30px 20px; }}
        h1 {{ font-size: 2.2em; }}
        .subtitle {{ font-size: 1.1em; }}
        body {{ background-attachment: scroll; }} /* Allow scrolling on mobile */
    }}
    """

    # --- HTML Content (same as before) ---
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
    # Use a height that fills more of the screen
    st.components.v1.html(homepage_html, height=750, scrolling=False) # Disable scrolling if possible
    st.write("DEBUGGING: Exiting show_landing_page_html()") # Debug print


# --- Helper Function to Show Main App (Step 3) ---
# (This function remains exactly the same as before)
def show_main_app():
    st.write("DEBUGGING: Entering show_main_app()") # Debug print
    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:
    """)
    # --- Sidebar Definition ---
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
    if 'current_module' in st.session_state:
        st.write(f"DEBUGGING: Displaying content for module: {st.session_state.current_module}")
        st.header(f"Module: {st.session_state.current_module}")
        st.info("Module content goes here...")
    else:
        st.write("DEBUGGING: No module selected yet.")
    st.write("DEBUGGING: Exiting show_main_app()")


# --- Page Routing Logic ---

# Check query param first (handles the "Get Started" click from HTML)
if st.query_params.get("start_app") == "true":
    st.write("DEBUGGING: Query param 'start_app=true' detected.")
    st.session_state.view_state = 'app'
    st.query_params.clear()
    st.write(f"DEBUGGING: view_state set to 'app', query params cleared.")

# Display content based on the current view state
current_state = st.session_state.get('view_state', 'landing') # Default to landing state
st.write(f"DEBUGGING: Routing based on view_state: {current_state}")

if current_state == 'app':
    show_main_app()

elif current_state == 'landing':
    # Call the function that shows the combined landing page
    show_landing_page_html(IMAGE_URL)

else:
    # Fallback if state is somehow invalid
    st.error(f"DEBUGGING: Invalid view_state encountered: {current_state}")
    st.session_state.view_state = 'landing' # Reset to default
    st.rerun()


# --- Optional: Hide Streamlit Elements during Landing ---
# You might want to keep this commented out initially or adjust which elements are hidden
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header[data-testid="stHeader"] {visibility: hidden;} /* Hide Streamlit's header */
#             </style>
#             """
# if st.session_state.get('view_state', 'landing') == 'landing':
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#     st.write("DEBUGGING: Applying CSS to hide Streamlit elements.")
# else:
#     st.write("DEBUGGING: Not applying CSS hiding (in app view).")
