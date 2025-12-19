CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    instructions TEXT NOT NULL
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_location TEXT
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER,
    ingredient_name TEXT NOT NULL,
    quantity REAL NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    PRIMARY KEY (recipe_id, ingredient_name)
);
