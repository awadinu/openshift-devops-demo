from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

VERSION = "1.0.0"
COLOR = "#2b6cb0"   # blue

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Pipeline App</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f7fafc;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 48px 64px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            text-align: center;
        }}
        .banner {{
            background: {color};
            color: white;
            padding: 12px 32px;
            border-radius: 8px;
            font-size: 24px;
            font-weight: bold;
        }}
        .version {{
            margin-top: 24px;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="banner">Hello from my pipeline!</div>
        <p class="version">version {version} — built by GitLab CI, running on OpenShift</p>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def root():
    return PAGE.format(color=COLOR, version=VERSION)

@app.get("/health")
def health():
    return {"status": "ok"}
