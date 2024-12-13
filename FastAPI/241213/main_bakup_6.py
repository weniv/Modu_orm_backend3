from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates


app = FastAPI(docs_url="/documentation", redoc_url=None)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
