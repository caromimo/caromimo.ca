import os
import pg8000.dbapi as dbapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiosql


app = FastAPI()


connection = dbapi.connect(
    host="localhost",
    database=os.environ["DATABASE"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/templates")

queries = aiosql.from_path("./app/queries.sql", "pg8000")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ids_and_titles = queries.get_ids_and_titles_of_recipes(connection)
    print(ids_and_titles)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "ids_and_titles": ids_and_titles,
        },
    )


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def read_recipe(request: Request, recipe_id):
    try:
        recipe_id = int(recipe_id)
    except ValueError:
        return templates.TemplateResponse(request=request, name="404.html")

    [
        title_en,
        image_path,
        description_en,
        source_en,
        ingredients,
        instructions_en,
    ] = queries.get_recipe_details(connection, recipe_id=recipe_id)
    print(instructions_en)
    return templates.TemplateResponse(
        request=request,
        name="recipe.html",
        context={
            "recipe_id": recipe_id,
            "title_en": title_en,
            "image_path": image_path,
            "source_en": source_en,
            "description_en": description_en,
            "ingredients_en": ingredients,
            "instructions_en": instructions_en,
        },
    )
