import streamlit as st
from PIL import Image
import io
import base64

def img_to_bytes(img_path):
    """Convert image to base64 bytes for HTML embedding"""
    img = Image.open(img_path)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

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
        @media (max-width: 768px) {
            .responsive-column {
                flex-direction: column;
            }
        }
        .homepage-image {
            max-width: 100%;
            height: auto;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header section
    header_col1, header_col2 = st.columns([0.7, 0.3])
    with header_col1:
        st.markdown("### Insights AI")
    with header_col2:
        st.markdown("<div style='text-align: right;'>"
                   "<a href='#' style='color: white; margin-left: 20px; text-decoration: none;'>Register</a>"
                   "<a href='#' style='color: white; margin-left: 20px; text-decoration: none;'>Login</a>"
                   "</div>", unsafe_allow_html=True)

    # Main content with responsive columns
    st.markdown("<div class='responsive-column'>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.6, 0.4], gap="medium")
    
    with col1:
        # Display the image using HTML embedding to avoid file path issues
        try:
            # Replace with your actual image path or use the base64 fallback
            img_bytes = img_to_bytes("SAMI_AI_UI_02.png")
            st.markdown(f"""
            <img src="data:image/png;base64,{img_bytes}" 
                 class="homepage-image" 
                 alt="SAMI AI Interface"/>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Couldn't load image: {str(e)}")
            # Fallback base64 image would go here
    
    with col2:
        # Content section
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
        
        # Centered button
        if st.button("Get Started", 
                    type="primary",
                    use_container_width=True,
                    key="start_button"):
            st.query_params["start_app"] = True
    
    st.markdown("</div>", unsafe_allow_html=True)

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
    
    Get started by selecting a module from the sidebar.
    """)
else:
    show_homepage()
