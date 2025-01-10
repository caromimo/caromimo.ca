-- name: get_recipe_details(recipe_id)^
-- Get all the details for a recipe
SELECT
    recipes.title_en,
    recipes.slug_en,
    recipe_images.image_path,
    recipes.description_en,
    recipes.source_en,
    ARRAY_AGG (
        json_build_object (
            'quantity',
            recipe_ingredients.quantity,
            'unit',
            recipe_ingredients.unit_en,
            'ingredient',
            ingredients.name_en
        )
    ) AS ingredients, 
    recipes.instructions_en
FROM
    recipes
    JOIN recipe_images ON recipes.recipe_id = recipe_images.recipe_id
    JOIN recipe_ingredients ON recipes.recipe_id = recipe_ingredients.recipe_id
    JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id
WHERE
    recipes.recipe_id = :recipe_id
GROUP BY
    recipes.title_en,
    recipes.slug_en,
    recipes.recipe_id,
    recipe_images.image_path,
    recipes.description_en,
    recipes.source_en,
    recipes.instructions_en;


-- name: get_ids_and_titles_of_recipes()
-- Get all the recipe ids and titles
SELECT recipe_id, title_en from recipes;