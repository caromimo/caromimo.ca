-- name: get_recipe_details(recipe_id)^
-- Get all the details for a recipe
SELECT recipes.title_en, recipe_images.image_path, recipes.description_en, ARRAY_AGG(ingredients.name_en order by ingredients.name_en), recipes.instructions_en 
    FROM recipes
    JOIN recipe_images ON recipes.recipe_id = recipe_images.recipe_id 
    JOIN recipe_ingredients ON recipes.recipe_id = recipe_ingredients.recipe_id
    JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.ingredient_id 
    WHERE recipes.recipe_id = :recipe_id
    GROUP BY recipes.recipe_id, recipes.title_en, recipe_images.image_path, recipes.description_en, recipes.instructions_en;