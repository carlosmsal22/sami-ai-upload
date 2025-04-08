import streamlit as st

# Configuration - use the raw GitHub URL for your image
IMAGE_URL = "https://raw.githubusercontent.com/yourusername/sami-ai-upload/main/images/robot-hand.png"
FALLBACK_IMAGE = "https://via.placeholder.com/600x400/37474F/ECEFF1?text=SAMI+AI"

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
        :root {
            --primary: #03A9F4;
            --dark-bg: linear-gradient(135deg, #37474F, #263238);
            --text-light: #ECEFF1;
            --text-muted: #B0BEC5;
        }
        .main {
            background: var(--dark-bg);
            color: var(--text-light);
        }
        .stButton>button {
            background-color: var(--primary);
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
            .image-container {
                padding: 0;
                margin-bottom: 20px;
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
    main_col1, main_col2 = st.columns([0.6, 0.4], gap="large")
    
    with main_col1:
        try:
            st.markdown(f"""
            <div class="image-container">
                <img src="{IMAGE_URL}" 
                     style="max-width:100%; max-height:70vh; object-fit: contain; border-radius: 8px;"/>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Image loading failed: {str(e)}")
            st.image(FALLBACK_IMAGE, use_container_width=True)
    
    with main_col2:
        st.markdown("<h1 style='color: #81D4FA; margin-top: 0;'>SAMI AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: var(--text-muted); font-size: 1.5em;'>EMPOWERING FUTURE TRENDS</p>", unsafe_allow_html=True)
        st.markdown("""
        <p style='line-height: 1.6; margin-bottom: 30px;'>
        Get AI-driven insights on emerging trends in markets, technology, 
        and consumer behavior. Ask questions, explore categories of responses, 
        and easily serve or export your findings.
        </p>
        """, unsafe_allow_html=True)
        
        if st.button("Get Started", type="primary", use_container_width=True):
            st.query_params["start_app"] = True

# App routing
if 'start_app' in st.query_params:
    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:
    """)
    st.success("Image successfully loaded from: " + IMAGE_URL)
else:
    show_homepage()
