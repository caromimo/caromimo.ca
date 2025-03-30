import yaml
import psycopg2
import os


# with open("recipes.yaml", "r") as data:
#     recipes = yaml.safe_load(data)
#     print(recipes)


def insert_recipe_data(recipe_data):
    conn = None  # Initialize conn outside the try block
    # Connect to the database
    conn = psycopg2.connect(
        host=os.environ["DATABASE_HOST"],
        database=os.environ["DATABASE"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
    )
    cur = conn.cursor()

    for recipe in recipe_data["recipes"]:
        print(recipe)
        # Insert recipe
        cur.execute(
            """
            INSERT INTO recipes (title_en, title_fr, slug_en, slug_fr, description_en, description_fr, source_en, source_fr,instructions_en, instructions_fr, prep_time_minutes, cook_time_minutes, servings)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING recipe_id;
            """,
            (
                recipe["title_en"],
                recipe["title_fr"],
                recipe["slug_en"],
                recipe["slug_fr"],
                recipe["description_en"],
                recipe["description_fr"],
                recipe["source_en"],
                recipe["source_fr"],
                recipe["instructions_en"],
                recipe["instructions_fr"],
                recipe["prep_time_minutes"],
                recipe["cook_time_minutes"],
                recipe["servings"],
            ),
        )
        recipe_id = cur.fetchone()[0]

        # Insert ingredients for the recipe
        for ingredient in recipe["ingredients"]:
            cur.execute(
                "SELECT ingredient_id FROM ingredients WHERE name_en = %s",
                (ingredient["name_en"],),
            )
            ingredient_row = cur.fetchone()
            if ingredient_row:
                ingredient_id = ingredient_row[0]
            else:
                cur.execute(
                    "INSERT INTO ingredients (name_en, name_fr) VALUES (%s, %s) RETURNING ingredient_id",
                    (ingredient["name_en"], ingredient["name_fr"]),
                )
                ingredient_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit_en, unit_fr) VALUES (%s, %s, %s, %s, %s)",
                (
                    recipe_id,
                    ingredient_id,
                    ingredient["quantity"],
                    ingredient["unit_en"],
                    ingredient["unit_fr"],
                ),
            )

        # Insert categories for the recipe
        for category in recipe["categories"]:
            cur.execute(
                "SELECT category_id FROM categories WHERE name_en = %s",
                (category["name_en"],),
            )
            category_row = cur.fetchone()
            if category_row:
                category_id = category_row[0]
            else:
                cur.execute(
                    "INSERT INTO categories (name_en, name_fr) VALUES (%s, %s) RETURNING category_id",
                    (category["name_en"], category["name_fr"]),
                )
                category_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (%s, %s)",
                (recipe_id, category_id),
            )

        # Insert images for the recipe
        for image in recipe["images"]:
            cur.execute(
                "INSERT INTO recipe_images (recipe_id, image_path, caption_en, caption_fr) VALUES (%s, %s, %s, %s)",
                (
                    recipe_id,
                    image["image_path"],
                    image["caption_en"],
                    image["caption_fr"],
                ),
            )

    # Commit the changes
    conn.commit()
    print("Recipes added successfully!")


if __name__ == "__main__":
    try:
        with open("recipes.yaml", "r") as f:
            recipe_data = yaml.safe_load(f)
        insert_recipe_data(recipe_data)
    except FileNotFoundError:
        print("Error: recipes.yaml file not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
