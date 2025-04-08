import streamlit as stimport streamlit as st
def show_homepage():
    base64_image = base64_image = "iVBORw0KGgoAAAANSUhEUgAAA8AAAAIcCAYAAAA5Xcd7AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxIAAAsSAdLdfvwAAP+lSURBVHhe7P1ns205mueH/YG19nHXm6zMrMoyXaarqntqejSmOS6C4guRoZAoM0PqG0ghEyFHSq/r4zBCb2UYIdEEqQgNxzQnht1dbctkZWWluzfzuuP2XoBeAA8W8MfCxnbHXvxu4O6DBffALmDBqR//L/5jiwilVKzNUKpL9DpxDSjV+7+M13v/FOk9BjrR19DeX0b8FXmsTsOxorVpeIrsjXA4Ir+LH8cj+EP+19CV9K5hyHmH5f5xeCFdKihF6bal3MK2/nB81mXb8DeFyx3LUUpvLv/WphWQ85/9tTqtv5YKULm+On3H/pk0fI4X01F9tzaNj5L6K2L4dOByLnD7c9WwPIbix/kHymeG3SNLv+0SoOae85fDZ3Ro/zievjyRd7bin6nIty21+Nfg8svU/M/T1+PTa3S/PJwSF5V+HK9aOhQpxd9TTJ8KVvv08+6N12uTljdOn7H8OjiezMbx9uThJ9osfK4/7H5tSumrTAjbxVHimabPwB0ISb9i+U3Ti+MnSHsv5qH95/6VD4exsVtrxvdJJX1r6b8OY/ijH1lyUfqbyvuA428xpHrj0oPflxKuIQE4fMnf0b4vA96U5eP0Gfvz0+0/w/0Pwaqxbhlri/nHxPk3lt+yo2mpxvYi+CHyc/krpJ9Qax8K0S8SxjdUr0TP/SehFA6Xd+4vMpyW3P6wOcP9U2vT8svywIdhzABrLaxWW/X5ufxUaluj0Wg0Go1Go9FoNBq3gzYAbjQatx6l1IWoRqPRaDQajcbNog2AG41Go9FoNBo3EmttphqNRmMZ3Tu//w9/Gj/IZjWsBqCC6qAiHWCMgrWjUgBgrV+bbr0t/8zCjbmtGhWFp61zwWvYBRV2I0yjfXhiK8Qn+MfxS9UYfw5HYiyWxV6UPnb9WaF17TOcThL/Ell4y61HuHhn7jeE/WH9qmzqbldsHD6Vu+l8yNO7ssU2y392n+05pQI01hdX/rk+ZPsvqJpk4RFT8sVKw9chmmEVMaV9EFWC/b0oOByRPyjWq9RNDcsJvDTWO0Da+7CZiC0sD9+/AXKHUp7ofVLxjn25hmwpYck5b1YqWDTWlZCiuuCBgNvjtnoYXH+rLisWSvGzkP6G14fylxY4ZbWro/7f+kyHvyrsuiYBm7P7GnHaKyzxICl/UprgXEV1OHfuJSyWX34+DfdrRr37Y8z3sn/GmrH9FLESGzk1801IJKQA+P0BpbN3Q1LGOWE4na3PF0U57fVZanF7LPg/2b7zt4wNfpDL8D4phMcoBD/sEtvcnqwLx0+Q9kJQPmbSSoTwMg9YisxCAmdnjdy6l8Tne8hhsrhq/2mVPknM8tjlcP+PfWBTeBtjHeig4jEXl/8K7H+bAW40Go1Go9FoLEHnhwBdE6wxicoPD2w0Go2UnbdmRq2nLhqZaEZBtstC5GC1Kiz3pvJvGn7jtmJSpbxaEaVVoi4a/mKeKwulbBYvpe20ytyvp9bFknrbaO1PhTXrX+Pt4qrqj1G+Ja31P7Ysv0V/BfF/y3CEy07Hrdlx/Jnrmx7UTwlqNdjVeq5Xp9Qn4HpTLee3Dk75i8qB5XD7ufMB8HXlthY23vdSVSZVjZsF52ejcV2YusKg0WisxlXWH36vlN8tl99p3SXx4O56DvRuF1ymWI32TKZuOrchDrcd9cP/8D9KWroO6T2hGfSFY91ZH74HlL+YsF6QAWztJSH3lBrl9w5E+inYv3J8pgvzeO+x6J17aVxL8RFKS9g3bZxr4fE9XDU4Pfh+2m2pyVtjW/fZntYdU5OP05dh91x/uJHVYu6/Do/xMwB0dj82M97z7dxn4dfiUykfnN7xPXI62YNfYroeMrV0Day7pG/Nr+75R6b1wuOOKLdXtaV+7J7jm5kTo7kvT4kpYXX1HkKWvwbfM7guHL9wn6Onln7M2vfE8j2f/n7JOs4e+8/pt2361ODwBW53JJ4r1roAp08Nud836Nd0L0i6SX6uGs9V258Sbg98Hp7ouf6Ee4wL9Yf9KfUnAr78szvGTMY9J/dH6sd0OBIPfs75yPewjum+tAUKsFTc/+O4WWuTtJN0ZjmZZebhDt3ITtm2g+VM8XG3OgtX4iPP2R/Rc3vB9wILYovDYX8Tc6sz8xKc/hnKJGWi5C+3x4JRo2xctlaC6okJ7w1q/yO/lVbh/brw99taY5f2RXLZpuMzkpdbQdv1+ydMrf+VlYesHIp+Wg72P5N/Iv7WWgzDAFgLKLoHmN/ny8XP2s88tMaNwk58VVtHNW4W230lXdf+5VJrvBrXnC1fvo1G42rg98r675abgVmyBLUwFrxGXPM8mWj/uUxx2eL+aFDZwPDmcdlx4PJ807gK+Xc+ADZLFCoN0EUQhzPVwF2WPCX/eU16CZaz5F+Nbd03bjpTtXLKfDWU0om6aHjPca7c3t48noV4XfCeqhqr1v/bQmt/ahTKaaNxhfWH26lye7Vd+a3Hq9Ker0k9vGvIBb6vrFfXjmJ8VysPXG8uKt/jGc545lfSldXbA+fT8vy6KDj/L77HGnFZ0TV++TOiL0wDbDZdvwtKX7QajV3QylOj0Wg0Go3G9ab11W4W6of/wf8lybFsj5/sWfGPeQ03D2trewx5zT5PGskeVfk6k4dXRtvxq4uN/AD9XWKVPYicPjyoV3qMkKWvQJiID69J5z1AgsjP9rnCsf8Mm9f2BOfy7/abCcuzLtu63xbe08qsKx+nNyPloxTu8j3AgNXL9/izvKzn8r96eXDhc3mz5J7viZPy7WZ1x/Ivcq1Sry8Srn9MvgyK04tbkBT2n9vP2h5Wdp/tAYbbqzQ+SMsPy59Jz+bePecLt2dCbc9iJj/B5ZNh91e2B9iHy+mSQ+/TLP/dL3/MZXu7orYUlstHLXr8/hpWlVvKI5errH6lcDqtnX8h/svTYVW23QPMKE7/5dGBlveAD0/85Xzm2Ia917znMqv//nHwNzUvPc/iKfkd7LFEArdIDk4G8Zfjy3t9w/uVnpdYZh7vAS7Z4vd9HEvxO82b9P3N1dP6CHJ5CfEnSbh+sJwhftJ+pcawVCEN75FlAYly+i13V2Z8/4T0M7bYfy5C5Y/TU+D2R6nO5bdK3y3FYLP2a7o8l9KD0y/Eb3K2PG8fuD1d932alZ9KfWX/2T9un+HtFPcAE6ufseHIQ7vBTBVSu8ae1yn3NdjfcBddYqvR2AzbTutuNBqNRqPRuNbUxhiN68WtGgBfR3gAs86A/DpSOsyg0dgGRffqir6mGO2/EO5SLaMmT6PRaDSuBmMNzAqHMF0HrOHDoFofa1W4X32ReSp9+trEhF55ddzbA+fRKipwAf2rW5lDdsPZ3FWIm6PWNDUajfW44hYkXhpVWCbVaDSuPysv59wxyo7qpqFtqmKuf3yWb19qXB+4LF3QcKSxJepH/+Q/TrJK7gEtDSB5RkRxTq8I730o7SWUWRVZq857BBmRT+QfosXIVtXd8x5Fhmd5+EsT75WWeIk8vIcyhhtkTITH1JKf84up+c9wvm1LKd+Fmnw18xq19LloWP5a+na0uD7ec46J8pv5Xym/bJ7pK/V2LMPp4KroD58JIPYKg7Nt8yuTgwehkTycNlPU7NTM43bWGgvtf1cnTT/e08rhS/vEe3fZXoYyLm95j85asiKTtxruluQzKKxfTi7f8vaK8y7bY71m+LzHisnlS8njv2Mq+c/pMQXvQwPG+l91n5kX2hOC0431kk/rpx/XR/Y3hffwMuvGn9tnds/xtFhMl8hC+wvqp7B/jJiLb+Me3Gm5Sv1OIXNnpuVkf+IypqzzJyl3Pp24D8bhrUopniwtmwMTd/wmceT2Z9qMwzdKykLqP6eTIGclcP7lLG/Ps/pD74+4f74c54/x/Q0OZwou+1OU/MnShe4lFjg3BIm1xH/0j1zw+1RYUv8QxS2/x7zgruLfunC7VkrHEQNrLZRSid2pPb+MlH9jLTRX0HWh8Oqh3xImX7IbYKvXAKxHvJxi5QNBGo3GDcWQumx8uKp0rUSZrFPQaGzJLt6hjc1ZrwXIB4g3jXjCoDZ5cPNYNzcbjbebt2YAfFXwPo54wDv1Rem6c9Plb1wsamKfrlJ8V2++Z5b1vA9XVOYvKa27tVTHqouUf8ZhpOHpRLF5TTVuOvRBQz4sJB8YWse00bgK7MSewngGivVXiesr2vEgVWMwWAMzcX9tTQmsv61wv/Qi+6ZTe8kbq+HqW7QfPyrrJSVsu/pvijYAbjQajSvips+oNJax+iy/se6eelaNRuPiuKl7mVehra5oNJajfvRP/q9J9ZdZCf5qxHtbBd6TuC61e4N5j2PtK0Asn4nuApNuiM72MEazUHY9/+G/aDBG5fZkr2Stw8t7hDN/yH1N3hrs/7rwnqN14T2kTE2+mvm6cHpyJ5TNt4Xlr6Un1zeuH/U9wHyQRtpBz+xn9WV5fRzLJ/nrC77s+QjtjP8Gl9dLKuh+Nq2zffqcyONHeH8kfGvdHk2OtzNzMsR1XO7xFLg61/bgZvdw+udTYU3B94i6XcN5uAL7J3u7pFxLe8T2GHkfaEP1de0v7ZR+lXBr1L7C5/4vL+9M7j7FmZsQLylPNbhduSjq8i9PvyqV/K/NxBQ76bwHWGbTffkfy29aH5jN81fqqQ+Xwh9hfUotn696D/CARaJ38ZnaHuH03H/he2Cl2ZbH3M5JO8JyBHvLsyt3V9kDHNpJr+fXirU2i1MMh7cqHP60lKn/rqx1sMbN+obnSZpweWOfU/O4/LmycMV7gImh2ABMw+kqcDkvwXtOh+yMBgeni/VjCUUzv1l/yP+Kjd3tARa9b+9kD7B/OsafJfBk/m0Ht2ucH1OIjHH6Lat7k2wbj7dlDzAX4FVYsy5Oskm4jUbjEti28Ww0MuIyJX+bSK2GnVimuUqnotHYPTrrKN5W1u6AXzLSJzWyvLnSutTMG43GiDbKIFVtELcOoWFq6da4EWz6imR300rJ/lba89tpjU5rqM4paAVoha7T6LqpvbN6WpG/utOkUFZ6VEpZKGXd3t3OzVAr7U4pjBXv8Y390DoPo+vUUqX9nuKwX9iHG2RYe4+wS3efnFl+5IqpmROTe1wvHqvMpFpb/gxdUQL7P6UXptyx/cblwvlQUuuyrfvLwWoDq7mvt3t5d3U46NuKQTTLGQ1+5Zf7mlPPYmysJsyvnsutP7X02pbLicUyrl6Cdbjo/KjxdnzmazRuCbw3kA8KuEp4eVnOVTY3hTSKlnq9DTNvsudNT9yD2VgGD4gbjfLebVF8MA+rXcP+S3tmjFObwG3j29BOrkuW7xulz7h9Z2rwy0w9azQaq6N+95/yPcCuVpW+FvEeO96TWIW+Otb2AIP2"
    inlined_css = """
body {
    font-family: 'Roboto', sans-serif;
    margin: 0;
    background: linear-gradient(135deg, #37474F, #263238);
    color: #ECEFF1;
    display: flex; /* Enable flexbox for the body */
    min-height: 100vh; /* Ensure body takes at least full height */
}

.container {
    display: flex; /* Keep flex for image and content */
    width: 100%;
    height: 100vh; /* Make container take full viewport height */
    background-color: transparent;
    border-radius: 0;
    overflow: hidden;
    box-shadow: none;
}

.image-section {
    flex: 0 0 60%; /* Image takes 60% width */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.image-section > div { /* Target a potential wrapper div */
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.image-section img {
    max-width: 95%;
    max-height: 95%;
    object-fit: contain;
}

.content-section {
    flex: 0 0 40%; /* Content takes 40% width */
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center content vertically */
    align-items: flex-start;
    height: 100%; /* Fill container height */
    padding: 40px;
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

@media (max-width: 900px) {
    body {
        flex-direction: column;
        align-items: center;
    }
    .container {
        flex-direction: column;
        height: auto;
    }
    .image-section, .content-section {
        flex: 0 0 auto;
        width: 80%;
        padding: 30px;
        text-align: center;
        align-items: center;
    }
    .content-section {
        align-items: center;
    }
    .image-section img {
        max-width: 70%;
    }
    header {
        flex-direction: column;
        align-items: center;
        text-align: center;
        position: static;
        padding: 10px;
        width: 100%;
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
