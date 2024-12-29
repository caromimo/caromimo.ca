import os
from pg8000 import dbapi
from fastapi import FastAPI

app = FastAPI()

connection = dbapi.connect(
    host="localhost",
    database=os.environ["DATABASE"],
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWORD"],
)

cursor = connection.cursor()


@app.get("/recipes/{recipe_id}")
async def read_recipe(recipe_id):
    cursor.execute("SELECT TITLE, SOURCE FROM RECIPES WHERE ID = %s", (recipe_id,))
    results = cursor.fetchone()
    return {"recipe_id": results}
