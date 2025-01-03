import os
import pg8000.dbapi as dbapi
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# a more readable style of parameter handling in sql statements.
# https://github.com/tlocke/pg8000?tab=readme-ov-file#pg8000dbapiparamstyle
dbapi.paramstyle = "named"
connection = dbapi.connect(
    host="localhost",
    database=os.environ["DATABASE"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
)

app.mount("/static", StaticFiles(directory="./app/static"), name="static")

templates = Jinja2Templates(directory="./app/templates")


cursor = connection.cursor()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def read_recipe(request: Request, recipe_id):
    try:
        recipe_id = int(recipe_id)
    except ValueError:
        return templates.TemplateResponse(request=request, name="404.html")

    # Get recipe details
    cursor.execute(
        """
        SELECT recipes.title_en, recipe_images.image_path, recipes.description_en, recipes.instructions_en 
        FROM recipes 
        JOIN recipe_images ON recipes.recipe_id = recipe_images.recipe_id 
        WHERE recipes.recipe_id = :recipe_id;""",
        {"recipe_id": recipe_id},
    )
    if cursor.rowcount == 0:
        return templates.TemplateResponse(request=request, name="404.html")

    [title_en, image_path, description_en, instructions_en] = cursor.fetchone()
    return templates.TemplateResponse(
        request=request,
        name="recipe.html",
        context={
            "recipe_id": recipe_id,
            "title_en": title_en,
            "image_path": image_path,
            "description_en": description_en,
            "instructions_en": instructions_en,
        },
    )
