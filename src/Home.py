homepage_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        {inlined_css}
    </style>
</head>
<body>
    <div class="container">
        <div class="image-section">
            <img src="data:image/png;base64,{base64_image}" alt="Robot Hand">
        </div>
        <div class="content-section">
            <h1>SAMI AI</h1>
            <p>Some content here.</p>
        </div>
    </div>
</body>
</html>
"""
st.components.v1.html(homepage_html)
