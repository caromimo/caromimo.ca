-- Migration to create tables in the database

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT,
    instructions TEXT,
    source TEXT,
    tags TEXT[],
    image_path TEXT 
);
