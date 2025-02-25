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


# FUNCTIONS TO RETURN ENGLISH CONTENT


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    slugs_and_titles = queries.slugs_and_titles(connection)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "slugs_and_titles": slugs_and_titles,
        },
    )


@app.get("/recipes/{slug_en}", response_class=HTMLResponse)
async def read_recipe(request: Request, slug_en):
    try:
        slug_en = slug_en
    except ValueError:
        return templates.TemplateResponse(request=request, name="404.html")

    [
        title_en,
        slug_en,
        image_path,
        description_en,
        source_en,
        ingredients,
        instructions_en,
    ] = queries.get_recipe_details(connection, slug_en=slug_en)
    return templates.TemplateResponse(
        request=request,
        name="recipe.html",
        context={
            "slug_en": slug_en,
            "title_en": title_en,
            "image_path": image_path,
            "source_en": source_en,
            "description_en": description_en,
            "ingredients_en": ingredients,
            "instructions_en": instructions_en,
        },
    )


# FUNCTIONS TO RETURN FRENCH CONTENT


@app.get("/fr/", response_class=HTMLResponse)
async def index_fr(request: Request):
    slugs_et_titres = queries.slugs_et_titres(connection)
    print(slugs_et_titres)
    return templates.TemplateResponse(
        request=request,
        name="index_fr.html",
        context={
            "slugs_et_titres": slugs_et_titres,
        },
    )


@app.get("/recettes/{slug_fr}", response_class=HTMLResponse)
async def lire_recette(request: Request, slug_fr):
    try:
        slug_fr = slug_fr
    except ValueError:
        return templates.TemplateResponse(request=request, name="404.html")

    [
        title_fr,
        slug_fr,
        image_path,
        description_fr,
        source_fr,
        ingredients,
        instructions_fr,
    ] = queries.obtenir_details_recette(connection, slug_fr=slug_fr)
    return templates.TemplateResponse(
        request=request,
        name="recette.html",
        context={
            "slug_fr": slug_fr,
            "title_fr": title_fr,
            "image_path": image_path,
            "source_fr": source_fr,
            "description_fr": description_fr,
            "ingredients_fr": ingredients,
            "instructions_fr": instructions_fr,
        },
    )
