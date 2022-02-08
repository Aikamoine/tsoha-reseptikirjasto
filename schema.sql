CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    visible INTEGER
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    servings INTEGER,
    time INTEGER,
    visible INTEGER
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE units (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    ingredient_id INTEGER REFERENCES ingredients,
    unit_id INTEGER REFERENCES units,
    amount NUMERIC(7,2)
);

CREATE TABLE recipe_steps (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    step TEXT,
    number INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    stars INTEGER,
    comment TEXT
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    tag TEXT
);

CREATE TABLE shoppinglists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    amount NUMERIC(7,2)
);
