import streamlit as st
from streamlit_javascript import st_javascript  # For proper redirection

# Configuration
GITHUB_USER = "yourusername"  # Replace with your GitHub username
REPO_NAME = "sami-ai-upload"  # Your repository name
IMAGE_PATH = "images/robot-hand.png"  # Corrected image path
IMAGE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/main/{IMAGE_PATH}"
MAIN_APP_URL = "/"  # Or your specific app route

def show_homepage():
    # Page setup
    st.set_page_config(
        page_title="SAMI AI",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #37474F, #263238);
            color: #ECEFF1;
        }
        .stButton>button {
            background-color: #03A9F4;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 1.2em;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            filter: brightness(0.9);
            transform: translateY(-1px);
        }
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            padding: 20px;
        }
        @media (max-width: 768px) {
            .responsive-columns {
                flex-direction: column-reverse;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px; color: white;">
        <div style="font-size: 1.5em; font-weight: bold;">Insights AI</div>
        <div style="display: flex; gap: 20px;">
            <a href="#" style="color: white; text-decoration: none;">Register</a>
            <a href="#" style="color: white; text-decoration: none;">Login</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([0.6, 0.4], gap="large")
    
    with col1:
        try:
            st.markdown(f"""
            <div class="image-container">
                <img src="{IMAGE_URL}" 
                     style="max-width:100%; max-height:70vh; object-fit: contain; border-radius: 8px;"/>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.error("Image failed to load. Please check:")
            st.code(f"Image URL: {IMAGE_URL}")
    
    with col2:
        st.markdown("<h1 style='color: #81D4FA; margin-top: 0;'>SAMI AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #B0BEC5; font-size: 1.5em;'>EMPOWERING FUTURE TRENDS</p>", unsafe_allow_html=True)
        st.markdown("""
        <p style='line-height: 1.6; margin-bottom: 30px;'>
        Get AI-driven insights on emerging trends in markets, technology, 
        and consumer behavior. Ask questions, explore categories of responses, 
        and easily serve or export your findings.
        </p>
        """, unsafe_allow_html=True)
        
        if st.button("Get Started", type="primary", use_container_width=True):
            # Proper page navigation
            js = f"window.location.href = '{MAIN_APP_URL}'"
            st_javascript(js)

# App routing
if 'start_app' in st.query_params:
    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:
    """)
else:
    show_homepage()
