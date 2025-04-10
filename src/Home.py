import streamlit as st
import base64

# --- Configuration ---
st.set_page_config(
    layout="wide",
    page_title="SAMI AI",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed for landing
)

# --- Base64 Image Data (Ensure this is the FULL string) ---
# Placeholder - Replace with your actual, complete base64 string
base64_robot_hand_image = "iVBORw0KGgoAAAANSUhEUgAAA8AAAAIcCAYAAAA5Xcd7AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxIAAAsSAdLdfvwAAP+lSURBVHhe7P1ns205mueH/YG19nHXm6zMrMoyXaarqntqejSmOS6C4guRoZAoM0PqG0ghEyFHSq/r4zBCb2UYIdEEqQgNxzQnht1dbctkZWWluzfzuuP2XoBeAA8W8MfCxnbHXvxu4O6DBffALmDBqR//L/5jiwilVKzNUKpL9DpxDSjV+7+M13v/FOk9BjrR19DeX0b8FXmsTsOxorVpeIrsjXA4Ir+LH8cj+EP+19CV9K5hyHmH5f5xeCFdKihF6bal3MK2/nB81mXb8DeFyx3LUUpvLv/WphWQ85/9tTqtv5YKULm+On3H/pk0fI4X01F9tzaNj5L6K2L4dOByLnD7c9WwPIbix/kHymeG3SNLv+0SoOae85fDZ3Ro/zievjyRd7bin6nIty21+Nfg8svU/M/T1+PTa3S/PJwSF5V+HK9aOhQpxd9TTJ8KVvv08+6N12uTljdOn7H8OjiezMbx9uThJ9osfK47H5tSumrTAjbxVHimabPwB0ISb9i+U3Ti+MnSHsv5qH95/6VD4exsVtrxvdJJX1r6b8OY/ijH1lyUfqbyvuA428xpHrj0oPflxKuIQE4fMnf0b4vA96U5eP0Gfvz0+0/w/0Pwaqxbhlri/nHxPk3lt+yo2mpxvYi+CHyc/krpJ9Qax8K0S8SxjdUr0TP/SehFA6Xd+4vMpyW3P6wOcP9U2vT8svywIdhzABrLaxWW/X5ufxUaluj0Wg0Go1Go9FoNBq3gzYAbjQatx6l1IWoRqPRaDQajcbNog2AG41Go9FoNBo3EmttphqNRmMZ3Tu//w9/Gj/IZjWsBqCC6qAiHWCMgrWjUgBgrV+bbr0t/8zCjbmtGhWFp61zwWvYBRV2I0yjfXhiK8Qn+MfxS9UYfw5HYiyWxV6UPnb9WaF17TOcThL/Ell4y61HuHhn7jeE/WH9qmzqbldsHD6Vu+l8yNO7ssU2y392n+05pQI01hdX/rk+ZPsvqJpk4RFT8sVKw9chmmEVMaV9EFWC/b0oOByRPyjWq9RNDcsJvDTWO0Da+7CZiC0sD9+/AXKHUp7ofVLxjn25hmwpYck5b1YqWDTWlZCiuuCBgNvjtnoYXH+rLisWSvGzkP6G14fylxY4ZbWro/7f+kyHvyrsuiYBm7P7GnHaKyzxICl/UprgXEV1OHfuJSyWX34+DfdrRr37Y8z3sn/GmrH9FLESGzk1801IJKQA+P0BpbN3Q1LGOWE4na3PF0U57fVZanF7LPg/2b7zt4wNfpDL8D4phMcoBD/sEtvcnqwLx0+Q9kJQPmbSSoTwMg9YisxCAmdnjdy6l8Tne8hhsrhq/2mVPknM8tjlcP+PfWBTeBtjHeig4jEXl/8K7H+bAW40Go1Go9FoLEHnhwBdE6wxicoPD2w0Go2UnbdmRq2nLhqZaEZBtstC5GC1Kiz3pvJvGn7jtmJSpbxaEaVVoi4a/mKeKwulbBYvpe20ytyvp9bFknrbaO1PhTXrX+Pt4qrqj1G+Ja31P7Ysv0V/BfF/y3CEy07Hrdlx/Jnrmx7UTwlqNdjVeq5Xp9Qn4HpTLee3Dk75i8qB5XD7ufMB8HXlthY23vdSVSZVjZsF52ejcV2YusKg0WisxlXWH36vlN8tl99p3SXx4O56DvRuF1ymWI32TKZuOrchDrcd9cP/8D9KWroO6T2hGfSFY91ZH74HlL+YsF6QAWztJSH3lBrl9w5E+inYv3J8pgvzeO+x6J17aVxL8RFKS9g3bZxr4fE9XDU4Pfh+2m2pyVtjW/fZntYdU5OP05dh91x/uJHVYu6/Do/xMwB0dj82M97z7dxn4dfiUykfnN7xPXI62YNfYroeMrV0Day7pG/Nr+75R6b1wuOOKLdXtaV+7J7jm5kTo7kvT4kpYXX1HkKWvwbfM7guHL9wn6Onln7M2vfE8j2f/n7JOs4e+8/pt2361ODwBW53JJ4r1roAp08Nud836Nd0L0i6SX6uGs9V258Sbg98Hp7ouf6Ee4wL9Yf9KfUnAr78szvGTMY9J/dH6sd0OBIPfs75yPewjum+tAUKsFTc/+O4WWuTtJN0ZjmZZebhDt3ITtm2g+VM8XG3OgtX4iPP2R/Rc3vB9wILYovDYX8Tc6sz8xKc/hnKJGWi5C+3x4JRo2xctlaC6okJ7w1q/yO/lVbh/brw99taY5f2RXLZpuMzkpdbQdv1+ydMrf+VlYesHIp+Wg72P5N/Iv7WWgzDAFgLKLoHmN/ny8XP2s88tMaNwk58VVtHNW4W230lXdf+5VJrvBrXnC1fvo1G42rg98r675abgVmyBLUwFrxGXPM8mWj/uUxx2eL+aFDZwPDmcdlx4PJ807gK+Xc+ADZLFCoN0EUQhzPVwF2WPCX/eU16CZaz5F+Nbd03bjpTtXLKfDWU0om6aHjPca7c3t48noV4XfCeqhqr1v/bQmt/ahTKaaNxhfWH26lye7Vd+a3Hq9Ker0k9vGvIBb6vrFfXjmJ8VysPXG8uKt/jGc545lfSldXbA+fT8vy6KDj/L77HGnFZ0TV++TOiL0wDbDZdvwtKX7QajV3QylOj0Wg0Go3G9ab11W4W6of/wf8lybFsj5/sWfGPeQ03D2trewx5zT5PGskeVfk6k4dXRtvxq4uN/AD9XWKVPYicPjyoV3qMkKWvQJiID69J5z1AgsjP9rnCsf8Mm9f2BOfy7/abCcuzLtu63xbe08qsKx+nNyPloxTu8j3AgNXL9/izvKzn8r96eXDhc3mz5J7viZPy7WZ1x/Ivcq1Sry8Srn9MvgyK04tbkBT2n9vP2h5Wdp/tAYbbqzQ+SMsPy59Jz+bePecLt2dCbc9iJj/B5ZNh91e2B9iHy+mSQ+/TLP/dL3/MZXu7orYUlstHLXr8/hpWlVvKI5errH6lcDqtnX8h/svTYVW23QPMKE7/5dGBlveAD0/85Xzm2Ia917znMqv//nHwNzUvPc/iKfkd7LFEArdIDk4G8Zfjy3t9w/uVnpdYZh7vAS7Z4vd9HEvxO82b9P3N1dP6CHJ5CfEnSbh+sJwhftJ+pcawVCEN75FlAYly+i13V2Z8/4T0M7bYfy5C5Y/TU+D2R6nO5bdK3y3FYLP2a7o8l9KD0y/Eb3K2PG8fuD1d932alZ9KfWX/2T9un+HtFPcAE6ufseHIQ7vBTBVSu8ae1yn3NdjfcBddYqvR2AzbTutuNBqNRqPRuNbUxhiN68WtGgBfR3gAs86A/DpSOsyg0dgGRffqir6mGO2/EO5SLaMmT6PRaDSuBmMNzAqHMF0HrOHDoFofa1W4X32ReSp9+trEhF55ddzbA+fRKipwAf2rW5lDdsPZ3FWIm6PWNDUajfW44hYkXhpVWCbVaDSuPysv59wxyo7qpqFtqmKuf3yWb19qXB+4LF3QcKSxJepH/+Q/TrJK7gEtDSB5RkRxTq8I730o7SWUWRVZq857BBmRT+QfosXIVtXd8x5Fhmd5+EsT75WWeIk8vIcyhhtkTITH1JKf84up+c9wvm1LKd+Fmnw18xq19LloWP5a+na0uD7ec46J8pv5Xym/bJ7pK/V2LMPp4KroD58JIPYKg7Nt8yuTgwehkTycNlPU7NTM43bWGgvtf1cnTT/e08rhS/vEe3fZXoYyLm95j85asiKTtxruluQzKKxfTi7f8vaK8y7bY71m+LzHisnlS8njv2Mq+c/pMQXvQwPG+l91n5kX2hOC0431kk/rpx/XR/Y3hffwMuvGn9tnds/xtFhMl8hC+wvqp7B/jJiLb+Me3Gm5Sv1OIXNnpuVkf+IypqzzJyl3Pp24D8bhrUopniwtmwMTd/wmceT2Z9qMwzdKykLqP6eTIGclcP7lLG/Ps/pD74+4f74c54/x/Q0OZwou+1OU/MnShe4lFjg3BIm1xH/0j1zw+1RYUv8QxS2/x7zgruLfunC7VkrHEQNrLZRSid2pPb+MlH9jLTRX0HWh8Oqh3xImX7IbYKvXAKxHvJxi5QNBGo3GDcWQumx8uKp0rUSZrFPQaGzJLt6hjc1ZrwXIB4g3jXjCoDZ5cPNYNzcbjbebt2YAfFXwPo54wDv1Rem6c9Plb1wsamKfrlJ8V2++Z5b1vA9XVOYvKa27tVTHqouUf8ZhpOHpRLF5TTVuOvRBQz4sJB8YWse00bgK7MSewngGivVXiesr2vEgVWMwWAMzcX9tTQmsv61wv/Qi+6ZTe8kbq+HqW7QfPyrrJSVsu/pvijYAbjQajSvips+oNJax+iy/se6eelaNRuPiuKl7mVehra5oNJajfvRP/q9J9ZdZCf5qxHtbBd6TuC61e4N5j2PtK0Asn4nuApNuiM72MEazUHY9/+G/aDBG5fZkr2Stw8t7hDN/yH1N3hrs/7rwnqN14T2kTE2+mvm6cHpyJ5TNt4Xlr6Un1zeuH/U9wHyQRtpBz+xn9WV5fRzLJ/nrC77s+QjtjP8Gl9dLKuh+Nq2zffqcyONHeH8kfGvdHk2OtzNzMsR1XO7xFLg61/bgZvdw+udTYU3B94i6XcN5uAL7J3u7pFxLe8T2GHkfaEP1de0v7ZR+lXBr1L7C5/4vL+9M7j7FmZsQLylPNbhduSjq8i9PvyqV/K/NxBQ76bwHWGbTffkfy29aH5jN81fqqQ+Xwh9hfUotn696D/CARaJ38ZnaHuH03H/he2Cl2ZbH3M5JO8JyBHvLsyt3V9kDHNpJr+fXirU2i1MMh7cqHP60lKn/rqx1sMbN+obnSZpweWOfU/O4/LmycMV7gImh2ABMw+kqcDkvwXtOh+yMBgeni/VjCUUzv1l/yP+Kjd3tARa9b+9kD7B/OsafJfBk/m0Ht2ucH1OIjHH6Lat7k2wbj7dlDzAX4FVYsy5Oskm4jUbjEti28Ww0MuIyJX+bSK2GnVimuUqnotHYPTrrKN5W1u6AXzLSJzWyvLnSutTMG43GiDbKIFVtELcOoWFq6da4EWz6imR300rJ/lba89tpjU5rqM4paAVoha7T6LqpvbN6WpG/utOkUFZ6VEpZKGXd3t3OzVAr7U4pjBXv8Y390DoPo+vUUqX9nuKwX9iHG2RYe4+wS3efnFl+5IqpmROTe1wvHqvMpFpb/gxdUQL7P6UXptyx/cblwvlQUuuyrfvLwWoDq7mvt3t5d3U46NuKQTTLGQ1+5Zf7mlPPYmysJsyvnsutP7X02pbLicUyrl6Cdbjo/KjxdnzmazRuCbw3kA8KuEp4eVnOVTY3hTSKlnq9DTNvsudNT9yD2VgGD4gbjfLebVF8MA+rXcP+S3tmjFObwG3j29BOrkuW7xulz7h9Z2rwy0w9azQaq6N+95/yPcCuVpW+FvEeO96TWIW+Otb2AIP2"

# --- Initialize Session State ---
# This determines which view is shown: 'image', 'content', or 'app'
if 'view_state' not in st.session_state:
    st.session_state.view_state = 'image' # Start with the image

# --- Helper Function to Show Content Block (Step 2) ---
def show_content_block_html():
    inlined_css = """
    body {
        /* Basic styles - adjust if needed */
        font-family: 'Roboto', sans-serif;
        margin: 0;
        color: #333; /* Default text color */
        display: flex; /* Use flexbox for centering */
        align-items: center; /* Vertical centering */
        justify-content: center; /* Horizontal centering */
        min-height: 95vh; /* Make body take full viewport height */
        box-sizing: border-box;
        background-color: #ffffff; /* White background for the content block area */
    }

    .content-container {
        /* Styles for the central content box */
        background-color: #f8f9fa; /* Light grey background for the box */
        padding: 40px 60px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        max-width: 700px; /* Max width of the content box */
        width: 90%; /* Responsive width */
        text-align: center; /* Center text inside the box */
        margin-top: 20px; /* Add some top margin */
    }

    header {
        /* Styles for the top "Insights AI | Register | Login" */
        position: absolute; /* Position it relative to the viewport */
        top: 20px;
        left: 0;
        width: 100%;
        padding: 0 40px; /* Padding on sides */
        display: flex;
        justify-content: space-between; /* Space out logo and nav */
        align-items: center;
        box-sizing: border-box;
        z-index: 10;
    }

    .logo {
        font-size: 1.4em;
        font-weight: bold;
        color: #555;
    }

    nav a {
        color: #007bff; /* Blue link color */
        text-decoration: none;
        margin-left: 20px;
        font-size: 1em;
    }

    nav a:hover {
        text-decoration: underline;
    }

    h1 {
        font-size: 2.8em;
        margin-bottom: 10px;
        color: #333;
    }

    .subtitle {
        font-size: 1.3em;
        color: #6c757d; /* Grey subtitle color */
        margin-bottom: 25px;
        font-weight: 400;
    }

    .description {
        line-height: 1.6;
        margin-bottom: 30px;
        font-size: 1em;
        color: #495057;
    }

    .get-started-button {
        background-color: #007bff; /* Blue button */
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 5px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
        text-decoration: none; /* Remove underline from link */
        display: inline-block; /* Make it behave like a button */
    }

    .get-started-button:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        header {
            padding: 0 20px;
            flex-direction: column; /* Stack logo and nav */
            text-align: center;
            position: static; /* Don't keep it absolute */
            margin-bottom: 30px;
        }
        nav {
            margin-top: 10px;
        }
        nav a {
            margin: 0 10px;
        }
        .content-container {
            padding: 30px 20px;
        }
        h1 {
            font-size: 2.2em;
        }
        .subtitle {
            font-size: 1.1em;
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
        <div class="content-container">
            <h1>SAMI AI</h1>
            <p class="subtitle">EMPOWERING FUTURE TRENDS</p>
            <p class="description">Get AI-driven insights on emerging trends in markets, technology, and consumer behavior. Ask questions, explore categorized responses, and easily save or export your findings.</p>
            <a href="/?start_app=true" class="get-started-button" target="_self">Get Started</a>
            <!-- target="_self" ensures it loads in the same tab -->
        </div>
    </body>
    </html>
    """
    # Use a height that likely encompasses the content, maybe allow scrolling
    st.components.v1.html(homepage_html, height=600, scrolling=True)

# --- Helper Function to Show Main App (Step 3) ---
def show_main_app():
    # Make sidebar visible again
    st.set_page_config(initial_sidebar_state="expanded")

    st.title("🤖 Welcome to SAMI AI")
    st.markdown("""
    Welcome to your all-in-one AI-powered research assistant.
    Use the sidebar to explore and analyze your data using advanced modules:
    """) # Removed the list for brevity, matches original-image.png

    # --- Sidebar Definition ---
    with st.sidebar:
        st.page_link("app.py", label="Home", icon="🏠") # Assuming your script is app.py
        st.markdown("---") # Separator
        st.subheader("Analysis Modules")
        # Use buttons or page links for navigation
        if st.button("CBC Conjoint"): st.session_state.current_module = "CBC"
        if st.button("CrossTabs Analyzer Phase1"): st.session_state.current_module = "CrossTabs1"
        if st.button("Enhanced CrossTabs Analyzer"): st.session_state.current_module = "CrossTabs2"
        if st.button("Executive Insight Generator old"): st.session_state.current_module = "ExecOld"
        if st.button("LCA Module"): st.session_state.current_module = "LCA"
        if st.button("MaxDiff Module"): st.session_state.current_module = "MaxDiff"
        if st.button("OLD CrossTabs Analyzer"): st.session_state.current_module = "OldCrossTabs1"
        if st.button("OLD CrossTabs Step2"): st.session_state.current_module = "OldCrossTabs2"
        if st.button("Persona From PPTX"): st.session_state.current_module = "PersonaPPTX"
        if st.button("Persona Generator"): st.session_state.current_module = "PersonaGen"
        if st.button("SAMI Analyzer"): st.session_state.current_module = "SAMI"
        if st.button("SEM Module"): st.session_state.current_module = "SEM"
        if st.button("Text Analytics"): st.session_state.current_module = "Text"
        if st.button("TURF Module"): st.session_state.current_module = "TURF"

    # --- Main Area Content (Based on Sidebar Selection) ---
    # You would add logic here to display the content for the selected module
    # For the initial "Welcome" screen, we don't need to check st.session_state.current_module yet
    # Example:
    # if 'current_module' in st.session_state:
    #    if st.session_state.current_module == "CBC":
    #        st.header("CBC Conjoint Module")
    #        # Add CBC specific widgets/content
    #    elif st.session_state.current_module == "CrossTabs1":
    #        st.header("CrossTabs Analyzer Phase 1")
            # Add CrossTabs1 specific widgets/content
        # etc.
    # else:
         # Optionally display something if no module is selected yet after landing
         # st.info("Select a module from the sidebar to begin.")
pass # Keep the welcome message visible


# --- Page Routing Logic ---

# Check query param first (handles the "Get Started" click)
if 'start_app' in st.query_params and st.query_params['start_app'] == 'true':
    st.session_state.view_state = 'app'
    # Use st.experimental_set_query_params to remove the param after reading it,
    # preventing it from sticking if the user navigates back/forward
    st.experimental_set_query_params()


# Display content based on the current view state
if st.session_state.view_state == 'app':
    show_main_app()

elif st.session_state.view_state == 'content':
    show_content_block_html()

elif st.session_state.view_state == 'image':
    # Display the image using the container width
    st.image(f"data:image/png;base64,{base64_robot_hand_image}", use_container_width=True) # <-- Change is here

    # Add a button *below* the image to trigger the transition to the content block
    # We use columns to center the button
    col1, col2, col3 = st.columns([2, 1, 2]) # Adjust ratios as needed for centering
    with col2:
        if st.button("Proceed", key="show_content_button", help="Click to see more options"):
            st.session_state.view_state = 'content'
            st.rerun() # Rerun the script to show the content block

# Optional: Add some CSS to hide Streamlit's default header/footer during landing
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header[data-testid="stHeader"] {visibility: hidden;} /* Hide new header */
            </style>
            """
# Only hide elements when not in the main app view
if st.session_state.view_state != 'app':
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
