def show_homepage():
    base64_image = "[YOUR_BASE64_ENCODED_ROBOT_HAND_IMAGE_STRING_HERE]"
    inlined_css = """
    body {
        font-family: 'Roboto', sans-serif; /* Use a common, clean font */
        margin: 0;
        background: linear-gradient(135deg, #37474F, #263238); /* Dark blue-grey gradient background */
        color: #ECEFF1; /* Light grey/white text color */
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh; /* Make the background cover the entire viewport */
        padding: 20px;
        box-sizing: border-box; /* Include padding and border in element's total width and height */
    }

    .container {
        display: flex;
        max-width: 1200px; /* Limit the maximum width of the content area */
        width: 100%; /* Make the container take full width up to the max-width */
        background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent dark background for content */
        border-radius: 10px; /* Slightly rounded corners */
        overflow: hidden; /* Prevent content from overflowing rounded corners */
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
    }

    .image-section {
        flex: 0 0 50%; /* Takes up 50% of the container width */
        display: flex;
        justify-content: center; /* Center the image horizontally */
        align-items: center; /* Center the image vertically */
        padding: 40px;
    }

    .image-section img {
        max-width: 80%; /* Ensure the image doesn't get too large */
        height: auto; /* Maintain image aspect ratio */
    }

    .content-section {
        flex: 0 0 50%; /* Takes up 50% of the container width */
        padding: 60px;
        display: flex;
        flex-direction: column; /* Stack content vertically */
        justify-content: center; /* Center content vertically */
        align-items: flex-start; /* Align text to the left */
    }

    h1 {
        font-size: 3em; /* Large heading */
        margin-bottom: 10px;
        color: #81D4FA; /* A light blue accent color for the title */
    }

    .subtitle {
        font-size: 1.5em; /* Slightly smaller subtitle */
        color: #B0BEC5; /* A lighter grey for the subtitle */
        margin-bottom: 20px;
    }

    .description {
        line-height: 1.6; /* Improve readability of the description */
        margin-bottom: 30px;
    }

    .get-started-button {
        background-color: #03A9F4; /* A brighter blue for the button */
        color: white;
        border: none;
        padding: 15px 30px; /* Comfortable padding inside the button */
        border-radius: 5px; /* Slightly rounded button corners */
        font-size: 1.2em;
        cursor: pointer; /* Change cursor to indicate it's clickable */
        transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        text-decoration: none; /* Remove underline from the link */
    }

    .get-started-button:hover {
        background-color: #0288D1; /* Darker shade of blue on hover */
    }

    /* Header (Logo and Navigation) */
    header {
        position: absolute;
        top: 20px;
        left: 20px;
        display: flex;
        justify-content: space-between; /* Space out logo and navigation */
        align-items: center;
        width: calc(100% - 40px); /* Adjust width for padding */
        color: white;
        z-index: 10; /* Ensure it's above other elements */
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
        color: #81D4FA; /* Light blue on hover for links */
    }

    /* Responsive Design (for smaller screens) */
    @media (max-width: 900px) {
        .container {
            flex-direction: column; /* Stack image and text vertically on smaller screens */
        }
        .image-section, .content-section {
            flex: 0 0 100%; /* Each takes full width */
            padding: 30px;
            text-align: center; /* Center text on smaller screens */
            align-items: center; /* Center items horizontally */
        }
        .content-section {
            align-items: center; /* Ensure content is centered */
        }
        .image-section img {
            max-width: 50%; /* Adjust image size on smaller screens */
        }
        header {
            flex-direction: column; /* Stack logo and navigation */
            align-items: center;
            text-align: center;
        }
        nav {
            margin-top: 10px;
        }
        nav a {
            margin: 0 10px;
        }
    }
    """
    homepage_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SAMI AI</title>
        <style>
            {inlined_css}
        </style>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
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
                <img src="data:image/png;base64,{base64_image}" alt="Robot Hand">
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
    st.components.v1.html(homepage_html, height=800) # Adjust height if needed

if 'start_app' in st.query_params:
    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:
    ... (rest of your Streamlit app content) ...
    """)
else:
    show_homepage()
