import streamlit as st

st.set_page_config(layout="wide")

def show_homepage():
    homepage_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAMI AI</title>
        <link rel="stylesheet" href="style.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                background: linear-gradient(135deg, #37474F, #263238);
                color: #ECEFF1;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
                box-sizing: border-box;
            }
            .container {
                display: flex;
                max-width: 1200px;
                width: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            }
            .image-section {
                flex: 0 0 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 40px;
            }
            .image-section img {
                max-width: 80%;
                height: auto;
            }
            .content-section {
                flex: 0 0 50%;
                padding: 60px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-start;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 10px;
                color: #81D4FA;
            }
            .subtitle {
                font-size: 1.5em;
                color: #B0BEC5;
                margin-bottom: 20px;
            }
            .description {
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .get-started-button {
                background-color: #03A9F4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 5px;
                font-size: 1.2em;
                cursor: pointer;
                transition: background-color 0.3s ease;
                text-decoration: none;
            }
            .get-started-button:hover {
                background-color: #0288D1;
            }
            header {
                position: absolute;
                top: 20px;
                left: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: calc(100% - 40px);
                color: white;
                z-index: 10;
            }
            .logo {
                font-size: 1.5em;
                font-weight: bold;
            }
            nav a {
                color: white;
                text-decoration: none;
                margin-left: 20px;
            }
            nav a:hover {
                color: #81D4FA;
            }
            /* Responsive Design */
            @media (max-width: 900px) {
                .container {
                    flex-direction: column;
                }
                .image-section, .content-section {
                    flex: 0 0 100%;
                    padding: 30px;
                    text-align: center;
                    align-items: center;
                }
                .content-section {
                    align-items: center;
                }
                .hero-image img {
                    max-width: 50%;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">Insights AI</div>
            <nav>
                <a href="#">Register</a>
                <a href="#">Login</a>
            </nav>
        </header>
        <div class="container">
            <div class="image-section">
                <img src="images/robot-hand.png" alt="Robot Hand">
            </div>
            <div class="content-section">
                <h1>SAMI AI</h1>
                <p class="subtitle">EMPOWERING FUTURE TRENDS</p>
                <p class="description">Get AI-driven insights on emerging trends in markets, technology, and consumer behavior. Ask questions, explore categorized responses, and easily save or export your findings.</p>
                <a href="/?start_app=true" class="get-started-button">Get Started</a>
            </div>
        </div>
    </body>
    </html>
    """
    st.components.v1.html(homepage_html, height=800) # Try removing height or increasing it

if 'start_app' in st.query_params:
    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:

    ### Available Modules:
    - 🧠 **SAMI Analyzer** – GPT-enhanced EDA and visualization
    - 📦 **CBC Conjoint** – Run choice-based modeling simulations
    - 🎯 **MaxDiff Module** – Prioritization using MaxDiff scaling
    - 🎯 **TURF Module** – Find optimal feature combinations
    - 🔍 **Text Analytics** – Extract insights from open-ended responses
    - 🧬 **LCA Module** – Latent Class segmentation
    - 🔗 **SEM Module** – Structural Equation Modeling
    - 📊 **CrossTabs Analyzer Phase 1** – Frequency, significance tests & stat tables
    - 📈 **CrossTabs Analyzer Phase 2** – GPT-based executive summary of crosstabs
    - 📄 **Executive Insight Generator** – Create slide-ready insight summaries
    - 🧬 **Persona Generator** – Extract buyer personas from segmentation
    - 🧬 **Persona From PPTX** – Generate personas from uploaded PPTX files

    ---

    💡 Upload your data in the respective module and let SAMI AI do the heavy lifting.
    """)
else:
    show_homepage()
