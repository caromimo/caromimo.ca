import os
from pg8000 import dbapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

connection = dbapi.connect(
    host="localhost",
    database=os.environ["DATABASE"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


cursor = connection.cursor()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def read_recipe(request: Request, recipe_id):
    cursor.execute("SELECT TITLE, SOURCE FROM RECIPES WHERE ID = %s", (recipe_id,))
    results = cursor.fetchone()
    return templates.TemplateResponse(
        request=request,
        name="recipe.html",
        context={"id": recipe_id, "results": results},
    )
