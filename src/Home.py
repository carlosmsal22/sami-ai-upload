import streamlit as st
import base64

# Your image converted to base64 (replace this with your actual image's base64 string)
BASE64_IMAGE = "iVBORw0KGgoAAAANSUhEUgAAA..."  # truncated example - put your full base64 string here

def show_homepage():
    # Configure page settings
    st.set_page_config(
        page_title="SAMI AI",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for styling
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
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0288D1;
            color: white;
        }
        .homepage-image {
            width: 100%;
            max-height: 80vh;
            object-fit: contain;
        }
        @media (max-width: 768px) {
            .responsive-column {
                flex-direction: column;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    with st.container():
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.markdown("### Insights AI")
        with col2:
            st.markdown("""
            <div style='text-align: right;'>
                <a href='#' style='color: white; margin-left: 20px; text-decoration: none;'>Register</a>
                <a href='#' style='color: white; margin-left: 20px; text-decoration: none;'>Login</a>
            </div>
            """, unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([0.6, 0.4], gap="medium")
    
    with col1:
        # Display the embedded base64 image
        st.markdown(f"""
        <img src="data:image/png;base64,{BASE64_IMAGE}" 
             class="homepage-image" 
             alt="SAMI AI Interface"/>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h1 style='color: #81D4FA; margin-top: 50px;'>SAMI AI</h1>", 
                   unsafe_allow_html=True)
        st.markdown("<p style='color: #B0BEC5; font-size: 1.5em;'>EMPOWERING FUTURE TRENDS</p>", 
                   unsafe_allow_html=True)
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
    - **Market Trends Analysis**
    - **Technology Forecasting**
    - **Consumer Behavior Insights**
    - **Data Visualization Tools**
    """)
else:
    show_homepage()
