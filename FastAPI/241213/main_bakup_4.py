from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <style>
        html, body {
            margin: 0;
            padding: 0;
        }
        div {
            margin: 0;
            padding: 0;
        }
        h1 {
            margin: 0;
            padding: 0;
            background-color: #4267B2;
            color: white;
        }
    </style>
</head>
<body>
    <div>
        <h1>facebook</h1>
    </div>
</body>
</html>
"""


@app.get("/about", response_class=HTMLResponse)
def about():
    return "<h1>hello world 2</h1>"


@app.get("/contact", response_class=HTMLResponse)
def contact():
    return "<h1>hello world 3</h1>"


@app.get("/notice", response_class=HTMLResponse)
def notice():
    return "<h1>hello world 4</h1>"
