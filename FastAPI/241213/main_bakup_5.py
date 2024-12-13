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


blog_post = [
    {
        "title": "첫번째 포스트",
        "contents": "첫번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-1",
    },
    {
        "title": "두번째 포스트",
        "contents": "두번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-2",
    },
    {
        "title": "세번째 포스트",
        "contents": "세번째 포스트 내용입니다.",
        "author": "이호준",
        "date": "2025-1-3",
    },
]

s = ""

for i in blog_post:
    s += f"""
    <section>
        <h2>{i['title']}</h2>
        <p>{i['contents']}</p>
        <p>{i['author']} | {i['date']}</p>
    </section>
    """


@app.get("/blog", response_class=HTMLResponse)
def notice():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
        }}
        div {{
            margin: 0;
            padding: 0;
        }}
        h1 {{
            margin: 0;
            padding: 0;
            background-color: #4267B2;
            color: white;
        }}
    </style>
</head>
<body>
    <header>
        <h1>hojun blog</h1>
    </header>
    <main>
        {s}
    </main>
    <footer>
        이호준 | 010-1234-1234 | hojun@gmail.com
    </footer>
</body>
</html>
"""
