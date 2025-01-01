-- Create the ingredients table:
CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name_en VARCHAR(255) UNIQUE NOT NULL,
    name_fr VARCHAR(255) UNIQUE NOT NULL
);

-- Create the categories table:
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name_en VARCHAR(255) UNIQUE NOT NULL,
    name_fr VARCHAR(255) UNIQUE NOT NULL
);

-- Create the recipes table:
CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    title_en VARCHAR(255) NOT NULL,
    title_fr VARCHAR(255) NOT NULL,
    description_en TEXT,
    description_fr TEXT,
    source_en TEXT,
    source_fr TEXT,
    instructions_en TEXT NOT NULL,
    instructions_fr TEXT NOT NULL,
    prep_time_minutes INT,
    cook_time_minutes INT,
    servings INT,
    date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    image_path VARCHAR(255)
);

-- Function to update the date_updated column
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_updated = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Trigger to execute the function before each update on the recipes table
CREATE TRIGGER update_recipes_modtime
    BEFORE UPDATE ON recipes
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();

-- Create the recipe_ingredients table: 
CREATE TABLE recipe_ingredients (
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    quantity VARCHAR(255),
    unit_en VARCHAR(50),
    unit_fr VARCHAR(50),
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
);

-- Create the recipe_categories table: 
CREATE TABLE recipe_categories (
    recipe_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (recipe_id, category_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

-- Create the recipe_images table: 
CREATE TABLE recipe_images (
    image_id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    caption_en VARCHAR(255),
    caption_fr VARCHAR(255),
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);