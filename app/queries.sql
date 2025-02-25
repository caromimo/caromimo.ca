-- name: get_recipe_details(slug_en)^
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
    recipes.slug_en = :slug_en
GROUP BY
    recipes.title_en,
    recipes.slug_en,
    recipes.recipe_id,
    recipe_images.image_path,
    recipes.description_en,
    recipes.source_en,
    recipes.instructions_en;


-- name: slugs_and_titles()
-- Get all the recipe ids and titles
SELECT slug_en, title_en from recipes;


-- name: obtenir_details_recette(slug_fr)^
-- Get all the details for a recipe in French
SELECT
    recipes.title_fr,
    recipes.slug_fr,
    recipe_images.image_path,
    recipes.description_fr,
    recipes.source_fr,
    ARRAY_AGG (
        json_build_object (
            'quantity',
            recipe_ingredients.quantity,
            'unit',
            recipe_ingredients.unit_fr,
            'ingredient',
            ingredients.name_fr
        )
    ) AS ingredients, 
    recipes.instructions_fr
FROM
    recipes
    JOIN recipe_images ON recipes.recipe_id = recipe_images.recipe_id
    JOIN recipe_ingredients ON recipes.recipe_id = recipe_ingredients.recipe_id
    JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id
WHERE
    recipes.slug_fr = :slug_fr
GROUP BY
    recipes.title_fr,
    recipes.slug_fr,
    recipes.recipe_id,
    recipe_images.image_path,
    recipes.description_fr,
    recipes.source_fr,
    recipes.instructions_fr;


-- name: slugs_et_titres()
-- Get all the recipe ids and titles in French
SELECT slug_fr, title_fr from recipes;