-- Migration to create tables in the database

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    ingredients JSONB,
    instructions JSONB,
    source TEXT,
    tags TEXT[]
);
