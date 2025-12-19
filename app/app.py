import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        instructions = request.form['instructions']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (name, instructions) VALUES (?, ?)', (name, instructions))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_recipe.html')

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
    ingredients = conn.execute('''
        SELECT
            ri.ingredient_name,
            ri.quantity,
            latest_costs.cost
        FROM recipe_ingredients ri
        JOIN (
            SELECT i1.name, i1.cost
            FROM ingredients i1
            JOIN (
                SELECT name, MAX(id) as max_id
                FROM ingredients
                GROUP BY name
            ) i2 ON i1.id = i2.max_id
        ) latest_costs ON ri.ingredient_name = latest_costs.name
        WHERE ri.recipe_id = ?
    ''', (recipe_id,)).fetchall()

    total_cost = sum(ingredient['cost'] * ingredient['quantity'] for ingredient in ingredients)

    all_ingredients = conn.execute('SELECT DISTINCT name FROM ingredients').fetchall()

    conn.close()

    return render_template('recipe.html', recipe=recipe, ingredients=ingredients, total_cost=total_cost, all_ingredients=all_ingredients)


@app.route('/recipe/<int:recipe_id>/add_ingredient', methods=['POST'])
def add_ingredient_to_recipe(recipe_id):
    ingredient_name = request.form['ingredient_name']
    quantity = request.form['quantity']

    conn = get_db_connection()
    conn.execute('INSERT INTO recipe_ingredients (recipe_id, ingredient_name, quantity) VALUES (?, ?, ?)',
                 (recipe_id, ingredient_name, quantity))
    conn.commit()
    conn.close()

    return redirect(url_for('recipe', recipe_id=recipe_id))


@app.route('/ingredients')
def ingredients():
    conn = get_db_connection()
    ingredients = conn.execute('SELECT * FROM ingredients ORDER BY purchase_date DESC').fetchall()
    conn.close()
    return render_template('ingredients.html', ingredients=ingredients)

@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient():
    if request.method == 'POST':
        name = request.form['name']
        cost = float(request.form['cost'])
        purchase_date = request.form['purchase_date']
        purchase_location = request.form['purchase_location']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO ingredients (name, cost, purchase_date, purchase_location) VALUES (?, ?, ?, ?)',
                     (name, cost, purchase_date, purchase_location))
        conn.commit()
        conn.close()
        
        return redirect(url_for('ingredients'))
    
    return render_template('add_ingredient.html')

if __name__ == '__main__':
    app.run(debug=True)
